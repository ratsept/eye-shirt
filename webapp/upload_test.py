import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/ronald/src/eye-shirt/webapp/uploads'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_PAGE = '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action="/upload" method=post enctype=multipart/form-data>
<p><input type=file name=file>
<input type=submit value=Upload>
</form>
'''

SHOW_IMAGE = '''
</br><img src="/uploads/uploaded_image.png"/>
'''

@app.route('/')
def main_page():
    return UPLOAD_PAGE


@app.route('/after_upload')
def after_upload():
    return UPLOAD_PAGE + SHOW_IMAGE


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    postfile = request.files['file']
    if postfile and allowed_file(postfile.filename):
        filename = secure_filename(postfile.filename)
        postfile.save(os.path.join(app.config['UPLOAD_FOLDER'],
                      'uploaded_image.png'))
        return redirect(url_for('after_upload'))
    else:
        return redirect(url_for('/'))

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

if __name__ == "__main__":
    app.run()
