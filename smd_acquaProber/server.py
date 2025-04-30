from flask import Flask, jsonify, render_template, request
import json
from sensor_reader import read_all_sensors, save_data

app = Flask(__name__)
DATA_FILE = 'data_log.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ph')
def ph_page():
    return render_template('ph.html')

@app.route('/turbidity')
def turbidity_page():
    return render_template('turbidity.html')

@app.route('/temperature')
def temperature_page():
    return render_template('temperature.html')

@app.route('/conductivity')
def conductivity_page():
    return render_template('conductivity.html')

@app.route('/api/data')
def get_last_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data_log = json.load(f)
            last_data = data_log[-1] if data_log else {}
    except (FileNotFoundError, json.JSONDecodeError):
        last_data = {}
    return jsonify(last_data)

@app.route('/api/history')
def get_history():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    return jsonify(data)

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    data = read_all_sensors()
    save_data(data)
    return jsonify({'status': 'success', 'data': data})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
