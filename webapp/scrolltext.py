import cv2
import numpy as np
import threading
import time


DEFAULT_STEP_SIZE = 3
DEFAULT_WINDOW_SIZE = (10, 10) # (h,w)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.35

class ScrollText:
    def __init__(self,
                 step_size = DEFAULT_STEP_SIZE,
                 window_size = DEFAULT_WINDOW_SIZE):
        self._window_size = window_size
        self._step_size = step_size
        self.frames = []

    def create_frames(self, text, color=(255, 255, 255)):
        text_size = cv2.getTextSize(text, FONT, FONT_SCALE, 1)
        img = np.zeros(
            (self._window_size[0], text_size[0][0] + 2*self._window_size[1], 3),
            dtype=np.uint8)
        cv2.putText(img, text, (self._window_size[1], 8), FONT,
                FONT_SCALE,
                color)      # BGR
        cv2.imwrite('/tmp/scrolltext_full.png', img)

        i = 0
        while i + self._window_size[1] < img.shape[1]:
            window = img[:, i:(i+self._window_size[1]), :]
            self.frames.append(window.copy())
            cv2.imwrite('/tmp/scrolltext_%04d.png' % i, window)
            i += self._step_size

FRAME_RATE = 1.0

class ScrollTextPlayer(threading.Thread):
    def __init__(self, connection, text):
        super(ScrollTextPlayer, self).__init__()

        self._connection = connection
        self._scrolltext = ScrollText()
        self._scrolltext.create_frames(text)
        self._stop = threading.Event()

        self.daemon = True
        self.start()

    def run(self):
        i = 0
        while not self._stop.is_set():
            self._connection.send_image(self._scrolltext.frames[i])
            i += 1
            i %= len(self._scrolltext.frames)
            time.sleep(1.0/FRAME_RATE)

    def stop(self):
        self._stop.set()


def main():
    ScrollText().create_frames('garage48', (255, 255, 255))

if __name__ == '__main__':
    main()
