from flask import redirect, render_template 
from flask import send_from_directory
from artwork import app
import os
import binascii


def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()

def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()

@app.route("/", methods=["GET", "POST"])
def index():
    artwork = []
    root_dir = app.config['ROOT_DIR'] + "/static/images/"
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                artwork.append(file)
    return render_template("index.html", paths=artwork, root_dir=root_dir)

@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)
