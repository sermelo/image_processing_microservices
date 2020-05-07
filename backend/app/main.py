from os import path, environ
from flask import Flask, request, send_from_directory, jsonify
import base64
import pickle
from processor import diff_tool
import cv2
import requests

HTML_DIR = 'html'
UPLOAD_FOLDER = '/var/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESS_FOLDER'] = UPLOAD_FOLDER
app.config['STORE'] = {'doit': environ.get('STORE').lower() == 'true',
                      'server': environ.get('STORAGE_SERVER')}

@app.route('/img/<path:filename>') 
def send_file(filename): 
    return send_from_directory(app.config['PROCESS'], filename)

@app.route("/api/process", methods=['POST'])
def process():
    uploaded_file1 = request.files["image1"]
    image1_path = path.join(app.config['UPLOAD_FOLDER'], uploaded_file1.filename)
    uploaded_file1.save(image1_path)

    uploaded_file2 = request.files["image2"]
    image2_path = path.join(app.config['UPLOAD_FOLDER'], uploaded_file2.filename)
    uploaded_file2.save(image2_path)

    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    image, boxes = diff_tool.diff(img1, img2)
    imdata = pickle.dumps(image)
    encoded_img = base64.encodebytes(imdata).decode("utf-8")
    json_response = {'image': encoded_img, 'boxes': boxes}
    if app.config['STORE']['doit']:
        files = {uploaded_file1.filename: base64.encodebytes(pickle.dumps(img1)).decode("utf-8"),
                 uploaded_file2.filename: base64.encodebytes(pickle.dumps(img2)).decode("utf-8"),
                 'diff.png': base64.encodebytes(pickle.dumps(image)).decode("utf-8")}
        store(files)
    
    return jsonify(json_response)

def store(files):
    server_url = app.config['STORE']['server']
    requests.post(server_url, files=files)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
