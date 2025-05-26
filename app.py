from flask import Flask, request, send_from_directory, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def gallery():
    images = os.listdir(UPLOAD_FOLDER)
    images.sort(reverse=True)  # newest first
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Image Gallery</title>
            <style>
                body { font-family: Arial; background: #f2f2f2; padding: 20px; }
                .gallery img { height: 150px; margin: 10px; border: 2px solid #ccc; }
            </style>
        </head>
        <body>
            <h1>Uploaded Images</h1>
            <div class="gallery">
                {% for img in images %}
                    <a href="/uploads/{{ img }}" target="_blank">
                        <img src="/uploads/{{ img }}">
                    </a>
                {% endfor %}
            </div>
        </body>
        </html>
    ''', images=images)

@app.route('/upload', methods=['POST'])
def upload_image():
    if request.data:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"image_{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "wb") as f:
            f.write(request.data)
        return "Image received", 200
    return "No data received", 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
