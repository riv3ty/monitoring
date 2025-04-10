from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins='*')

# Store connected agents and their metrics
agents = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected')

@socketio.on('metrics_update')
def handle_metrics_update(data):
    hostname = data.get('hostname')
    agents[hostname] = data
    socketio.emit('metrics_update', {'agents': list(agents.values())})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
