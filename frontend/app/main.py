from os import path, environ
from flask import Flask, request, send_from_directory
import requests
import base64
import pickle
import uuid
import numpy as np
import cv2
import pickle
from scipy import misc

HTML_DIR = 'html'
UPLOAD_FOLDER = '/var/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BACKEND_SERVER'] = environ.get('BACKEND_SERVER')


@app.route('/img/<path:filename>') 
def send_file(filename): 
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/uploader", methods=['GET', 'POST'])
def diff():
    # Save image 1 to file
    uploaded_file1 = request.files["image1"]
    file1_path = path.join(app.config['UPLOAD_FOLDER'], uploaded_file1.filename)
    uploaded_file1.save(file1_path)

    # Save image 2 to file
    uploaded_file2 = request.files["image2"]
    file2_path = path.join(app.config['UPLOAD_FOLDER'], uploaded_file2.filename)
    uploaded_file2.save(file2_path)

    # Requesto to backend the diff image
    backend_url = app.config['BACKEND_SERVER']
    files = {'image1': open(file1_path, 'rb'),
             'image2': open(file2_path, 'rb')}
    response = requests.post(backend_url, files=files)
    data = response.json()

    # Save diff image to file
    filename = f'{uuid.uuid1()}.png'  # I assume you have a way of picking unique filenames

    imgdata = base64.b64decode(data['image'])
    with open(path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
        f.write(imgdata)

    # Create the html page adding the box data and the diff image
    html_file = path.join(HTML_DIR, 'uploader.html')
    f = open(html_file, "r")
    html = f.read()
    html = html.replace('{box}', str(data['boxes']))
    html = html.replace('{image}', f'img/{filename}')
    return html

@app.route("/")
def main():
    html_file = path.join(HTML_DIR, 'main.html')
    f = open(html_file, "r")
    return f.read()

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
