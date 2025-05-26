from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server is running"

@app.route('/upload', methods=['POST'])
def upload_image():
    if request.data:
        with open("image.jpg", "wb") as f:
            f.write(request.data)
        return "Image received", 200
    return "No data received", 400

# Required for Render to detect the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
