from flask import Flask, request, redirect, url_for
import ledscreen_connection
import sys
import cv2
from PIL import Image
import numpy as np
import base64
from StringIO import StringIO

SCREEN_SIZE = (10, 20)

UPLOAD_PAGE = '''
<p><form action="/upload_image" method=post enctype=multipart/form-data>
<input type=file name=file>
<input type=submit value=Upload>
</form></p>
<p>
<p><form action="/upload_text" method=post>
<input type=text name=text> <input type=submit value="show text on screen">
</form></p>
'''

NO_CONNECTION_PAGE = '''
No connection to screen. <a href="/">Retry</a>
'''

INVALID_UPLOAD = '''
Uploaded file invalid. <a href="/">Retry</a>
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


@app.route('/invalid_upload')
def invalid_upload():
    return INVALID_UPLOAD


@app.route('/upload_image', methods=['POST'])
def upload_file():
    postfile = request.files['file']
    try:
        uploaded_img = np.array(Image.open(postfile))
    except:
        return redirect(url_for('invalid_upload'))

    cv2.imwrite('/tmp/uploaded.png', uploaded_img)
    screen_img = cv2.resize(uploaded_img, SCREEN_SIZE[::-1])

    if not screen_connection.connected:
        return redirect(url_for('upload_page'))

    screen_connection.send_image(screen_img)

    pngfile = StringIO()
    show_img = cv2.resize(screen_img, (200, 200),
                          interpolation=cv2.INTER_NEAREST)
    Image.fromarray(show_img).save(pngfile, 'PNG')

    return '''
        <img src="data:image/png;base64,%s"/><br>
        <a href="/">Upload page</a>
    ''' % base64.b64encode(pngfile.getvalue())


@app.route('/upload_text', methods=['POST'])
def upload_text():
    return ''


if __name__ == "__main__":
    app.run()
