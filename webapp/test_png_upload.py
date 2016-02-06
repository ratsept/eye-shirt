from ledscreen_connection import LedScreenConnection
import cv2
import sys
import time

img = cv2.imread(sys.argv[1])
assert img.shape == (10, 10, 3)

conn = LedScreenConnection('127.0.0.1')

while not conn.connected:
    time.sleep(0.1)
conn.send_image(img)
conn.keep_running = False
