from flask import Flask, render_template, jsonify, redirect, url_for, request, flash, session
from flask_socketio import SocketIO
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, UserLog
from telegram_notifier import TelegramNotifier
from dotenv import load_dotenv
import json
import os
import asyncio

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monitoring.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app, cors_allowed_origins='*')
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create database tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize Telegram notifier
notifier = TelegramNotifier()

# Store connected agents and their metrics
agents = {}

# Store agent status
agent_status = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if User.query.filter_by(username=username).first():
            flash('Benutzername bereits vergeben')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwörter stimmen nicht überein')
            return render_template('register.html')

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        UserLog.log_action(user.id, 'registered')
        flash('Registrierung erfolgreich')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Clear any existing session
    session.clear()
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            UserLog.log_action(user.id, 'logged_in')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
            
        flash('Ungültige Anmeldedaten')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        UserLog.log_action(current_user.id, 'logged_out')
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'Client connected from {request.sid}')
    # Note: The actual agent connection will be handled when we receive the first metrics

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print(f'Client disconnected: {sid}')
    
    # Find which agent disconnected
    disconnected_hostname = None
    for hostname, status in agent_status.items():
        if status.get('sid') == sid:
            disconnected_hostname = hostname
            break
    
    if disconnected_hostname:
        # Remove agent data
        agents.pop(disconnected_hostname, None)
        agent_status.pop(disconnected_hostname, None)
        
        # Send notification
        if notifier:
            asyncio.run(notifier.send_message(f'🔴 Agent {disconnected_hostname} went offline'))
        
        # Update all clients
        socketio.emit('metrics_update', {'agents': list(agents.values())})

@socketio.on('metrics_update')
def handle_metrics_update(data):
    print(f"Received metrics update from {request.sid}: {data}")
    try:
        hostname = data.get('hostname')
        if not hostname:
            print(f"Error: No hostname in data: {data}")
            return
        
        # Check if this is a new agent or reconnecting agent
        if hostname not in agents:
            if notifier:
                asyncio.run(notifier.send_message(f'🟢 Agent {hostname} is now online'))
        
        # Update agent data and status
        agents[hostname] = data
        agent_status[hostname] = {
            'last_seen': data.get('timestamp', 0),
            'sid': request.sid
        }
        
        print(f"Updated agents dict: {agents}")
        
        # Check thresholds and send notifications
        if notifier:
            try:
                asyncio.run(notifier.check_thresholds(hostname, data))
            except Exception as e:
                print(f"Error sending Telegram notification: {e}")
        
        response_data = {'agents': list(agents.values())}
        print(f"Emitting update to all clients: {response_data}")
        socketio.emit('metrics_update', response_data)
    except Exception as e:
        print(f"Error in handle_metrics_update: {str(e)}")
        print(f"Data was: {data}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5011, debug=True, allow_unsafe_werkzeug=True)
