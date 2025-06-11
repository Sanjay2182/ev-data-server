from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'gps_logs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def welcome():
    return "GPS Logger is running. POST data to /upload"

@app.route('/upload', methods=['POST'])
def upload_gps():
    data = request.get_json()
    if not data or 'gps' not in data:
        return jsonify({"status": "fail", "message": "No GPS data received"}), 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"gps_{timestamp}.txt"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "w") as f:
        f.write(data['gps'])

    return jsonify({"status": "success", "message": "GPS data received"}), 200

@app.route('/logs', methods=['GET'])
def list_logs():
    files = os.listdir(UPLOAD_FOLDER)
    files.sort(reverse=True)
    return jsonify(files)

@app.route('/logs/<filename>', methods=['GET'])
def get_log(filename):
    try:
        with open(os.path.join(UPLOAD_FOLDER, filename), 'r') as f:
            content = f.read()
        return jsonify({"filename": filename, "content": content})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
