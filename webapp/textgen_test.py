import cv2
import numpy as np

TEXT = "garage48"
WINDOW_SIZE = (10, 20)
STEP = 3
FONT = cv2.FONT_HERSHEY_PLAIN
FONT_SCALE = 0.7

text_size = cv2.getTextSize(TEXT, FONT, FONT_SCALE, 1)
print text_size
img = np.ones((10, text_size[0][0] + 2*WINDOW_SIZE[1], 3), dtype=np.uint8)*255

cv2.putText(img, TEXT, (WINDOW_SIZE[1], 8), FONT,
            FONT_SCALE,            # fontScale
            (255, 0, 0))    # BGR
cv2.imwrite('/tmp/test.png', img)

i = 0
while i + WINDOW_SIZE[1] < img.shape[1]:
    window = img[:, i:(i+WINDOW_SIZE[1]), :]
    cv2.imwrite('/tmp/text_%04d.png' % i, window)
    i += STEP
