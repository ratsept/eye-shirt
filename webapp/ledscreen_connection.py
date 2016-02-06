import socket
import threading
import time

PORT = 2000

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
                print 'connection failed, retrying in 1s'
                time.sleep(1)
                continue
            self.connected = True

            while self.keep_running:
                time.sleep(0.1)

            self._socket.close()
            self.connected = False

    def send_pixels(self, pixels):
        assert self.connected
        self._socket.send(pixels)
