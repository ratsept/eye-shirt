import socket
import threading
import time
import numpy as np

PORT = 2000

MAPPING_STR = '''
128 127 126 125 124 153 152 151 150 149
10  11  30  31  50  51  68  69  88  89
133 132 131 130 129 158 157 156 155 154
9   12  29  32  49  52  67  70  87  90
138 137 136 135 134 163 162 161 160 159
8   13  28  33  48  53  66  71  86  91
143 142 141 140 139 168 167 166 165 164
7   14  27  34  47  54  65  72  85  92
148 147 146 145 144 173 172 171 170 169
6   15  26  35  46  55  64  73  84  93
103 102 101 100 99  178 177 176 175 174
5   16  25  36  45  56  x   74  83  94
108 107 106 105 104 183 182 181 180 179
4   17  24  37  44  57  x   75  82  95
113 112 111 110 109 188 187 186 185 184
3   18  23  38  43  58  63  76  81  96
118 117 116 115 114 193 192 191 190 189
2   19  22  39  42  59  62  77  80  97
123 122 121 120 119 198 197 196 195 194
1   20  21  40  41  60  61  78  79  98
'''

_MAP_STR_LIST = filter(lambda s: s != '', MAPPING_STR.split('\n'))
_MAP = [s.split() for s in _MAP_STR_LIST]
MAP = [[int(s) if s != 'x' else None for s in row] for row in _MAP]
MAP_MAX = max([max(row) for row in MAP])


def screen_mapping(image):
    assert image.shape == (10, 20, 3)
    buf = [0, 0, 0]*MAP_MAX
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            addr = MAP[col][row]
            if addr:
                addr = (addr-1)*3
                buf[addr:addr+3] = image[row, col].tostring()
    return ''.join(buf)


class LedScreenConnection(threading.Thread):
    def __init__(self, screen_host):
        super(LedScreenConnection, self).__init__()
        # Code using this class may set keep_running False
        self.keep_running = True
        # Code using this class may read connected field
        self.connected = False

        self._socket = None
        self._host = screen_host

        self.daemon = True
        self.start()

    def run(self):
        while self.keep_running:
            try:
                self._socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
                self._socket.connect((self._host, PORT))
            except socket.error:
                print 'connection failed, retrying in 2s'
                time.sleep(2)
                continue
            print 'connected to led screen'
            self.connected = True

            while self.keep_running:
                time.sleep(0.1)

            self._socket.close()
            self.connected = False
            print 'connection lost'

    def send_image(self, image):
        assert self.connected
        self._buf = screen_mapping((image[:, ::-1, (1, 0, 2)]*0.2).astype(np.uint8))
        self._socket.send(self._buf)
