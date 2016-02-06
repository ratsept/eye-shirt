from flask import Flask, request, redirect, url_for
import ledscreen_connection
import sys
import cv2
from PIL import Image
import numpy as np

SCREEN_SIZE = (10, 10)

UPLOAD_PAGE = '''
<form action="/upload" method=post enctype=multipart/form-data>
<p><input type=file name=file>
<input type=submit value=Upload>
'''

NO_CONNECTION_PAGE = '''
No connection to screen. <a href="/">Retry</a>
'''

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

screen_connection = ledscreen_connection.LedScreenConnection(sys.argv[1])


@app.route('/')
def upload_page():
    if screen_connection and screen_connection.connected:
        return UPLOAD_PAGE
    else:
        return NO_CONNECTION_PAGE


@app.route('/upload', methods=['POST'])
def upload_file():
    postfile = request.files['file']
    uploaded_img = np.array(Image.open(postfile))
    cv2.imwrite('/tmp/uploaded.png', uploaded_img)
    screen_image = cv2.resize(uploaded_img, SCREEN_SIZE)
    assert screen_image.shape == SCREEN_SIZE + (3,)
    screen_connection.send_pixels(screen_image.tostring())
    return redirect(url_for('upload_page'))


if __name__ == "__main__":
    app.run()
