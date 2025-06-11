from flask import Flask, request, jsonify, render_template_string
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'gps_logs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

latest_gps_data = {}  # store last GPS entry

@app.route('/')
def home():
    # Serve an HTML page that shows latest GPS
    return render_template_string("""
    <html>
    <head>
        <title>GPS Tracker</title>
        <meta http-equiv="refresh" content="10"> <!-- refresh every 10 sec -->
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .card { background: white; padding: 20px; border-radius: 8px; max-width: 500px; margin: auto; }
            .map-link { margin-top: 10px; display: block; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Latest GPS Tracking Data</h2>
            {% if gps %}
                <p><strong>Timestamp:</strong> {{ gps.timestamp }}</p>
                <p><strong>Latitude:</strong> {{ gps.lat }}</p>
                <p><strong>Longitude:</strong> {{ gps.lon }}</p>
                <a class="map-link" href="https://www.google.com/maps?q={{ gps.lat }},{{ gps.lon }}" target="_blank">View on Google Maps</a>
            {% else %}
                <p>No GPS data received yet.</p>
            {% endif %}
        </div>
    </body>
    </html>
    """, gps=latest_gps_data or None)

@app.route('/upload', methods=['POST'])
def upload_gps():
    global latest_gps_data
    data = request.get_json()
    if not data or 'gps' not in data:
        return jsonify({"status": "fail", "message": "No GPS data received"}), 400

    gps_str = data['gps']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save to file
    filename = f"gps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(os.path.join(UPLOAD_FOLDER, filename), "w") as f:
        f.write(gps_str)

    # Parse latitude and longitude from the GPS string
    try:
        parts = gps_str.split(',')
        lat = float(parts[3])
        lon = float(parts[4])
        latest_gps_data = {
            "lat": lat,
            "lon": lon,
            "timestamp": timestamp
        }
    except Exception as e:
        print("Failed to parse GPS:", e)

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
