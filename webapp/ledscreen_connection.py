import socket
import threading
import time
import numpy as np

PORT = 2000


def screen_mapping(image):
    screendata = np.zeros(image.shape, dtype=np.uint8)
    for row in range(screendata.shape[0]):
        if row % 2:
            screendata[row] = image[row]
        else:
            screendata[row] = image[row, ::-1, :]
    return screendata


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
        self._socket.send(screen_mapping(image).tostring())
