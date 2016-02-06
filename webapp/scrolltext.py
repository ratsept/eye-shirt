import cv2
import numpy as np

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
            cv2.imwrite('/tmp/scrolltext_%04d.png' % i, window)
            i += self._step_size

def main():
    ScrollText().create_frames('garage48', (255, 255, 255))

if __name__ == '__main__':
    main()
