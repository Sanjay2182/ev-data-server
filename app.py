from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "EV Server is Live 🚗"

@app.route('/log', methods=['POST'])
def log_data():
    data = request.get_json()
    print("Received:", data)
    return "Data received successfully ✅"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
