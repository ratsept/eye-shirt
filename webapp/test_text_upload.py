from ledscreen_connection import LedScreenConnection
from scrolltext import ScrollTextPlayer
import sys
import time

conn = LedScreenConnection(sys.argv[1])
while not conn.connected:
    time.sleep(0.1)

player = ScrollTextPlayer(conn, sys.argv[2])

while conn.connected:
    time.sleep(0.1)
