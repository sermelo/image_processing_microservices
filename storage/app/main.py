from os import path, mkdir
from flask import Flask, request, jsonify
import uuid

UPLOAD_FOLDER = '/var/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/api/store", methods=['POST'])
def process():
    request_storage_dir = path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid1()))
    mkdir(request_storage_dir)
    for key in request.files:
        uploaded_file = request.files[key]
        uploaded_file.save(path.join(request_storage_dir, uploaded_file.filename))
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
