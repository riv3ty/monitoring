from flask import Flask, render_template, jsonify, redirect, url_for, request, flash
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins='*')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple user class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Hardcoded user (in production, use a database)
users = {'admin': {'password': 'admin123'}}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# Store connected agents and their metrics
agents = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        flash('Ungültige Anmeldedaten')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'Client connected from {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected')

@socketio.on('metrics_update')
def handle_metrics_update(data):
    print(f"Received metrics update from {request.sid}: {data}")
    try:
        hostname = data.get('hostname')
        if not hostname:
            print(f"Error: No hostname in data: {data}")
            return
        
        agents[hostname] = data
        print(f"Updated agents dict: {agents}")
        
        response_data = {'agents': list(agents.values())}
        print(f"Emitting update to all clients: {response_data}")
        socketio.emit('metrics_update', response_data)
    except Exception as e:
        print(f"Error in handle_metrics_update: {str(e)}")
        print(f"Data was: {data}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5011, debug=True, allow_unsafe_werkzeug=True)
