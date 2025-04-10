# System Monitoring Dokumentation

## Inhaltsverzeichnis
1. [Überblick](#überblick)
2. [Systemarchitektur](#systemarchitektur)
3. [Komponenten](#komponenten)
4. [Installation](#installation)
5. [Konfiguration](#konfiguration)
6. [Verwendung](#verwendung)
7. [Technische Details](#technische-details)
8. [Fehlerbehebung](#fehlerbehebung)

## Überblick
Das System Monitoring Tool ist eine Webanwendung zur Überwachung von Systemressourcen wie CPU, Arbeitsspeicher und Festplattennutzung. Es besteht aus einem zentralen Server und Agenten, die auf den zu überwachenden Systemen laufen.

### Hauptfunktionen
- Echtzeit-Überwachung von Systemressourcen
- Benutzerauthentifizierung für sicheren Zugriff
- Telegram-Benachrichtigungen bei kritischen Ereignissen
- Responsive Weboberfläche
- Multi-Agent-Unterstützung

## Systemarchitektur

### Server (server.py)
- Flask-Webanwendung
- Socket.IO für Echtzeit-Kommunikation
- SQLite-Datenbank für Benutzerverwaltung
- Telegram-Bot für Benachrichtigungen

### Agent (agent.py)
- Leichtgewichtiger Python-Client
- Sammelt Systemmetriken mit psutil
- Verbindet sich via Socket.IO mit dem Server
- Unterstützt Test-Modus für Simulationen

### Datenbank (models.py)
- SQLite mit SQLAlchemy ORM
- Benutzer- und Protokollierungstabellen
- Sichere Passwort-Hashing

## Komponenten

### Server-Komponenten

#### Flask-Routen
- \`/\`: Hauptseite mit Dashboard
- \`/login\`: Benutzeranmeldung
- \`/register\`: Benutzerregistrierung
- \`/logout\`: Abmeldung

#### Socket.IO-Events
- \`connect\`: Neue Client-Verbindung
- \`disconnect\`: Client-Trennung
- \`metrics_update\`: Empfang neuer Metriken

#### Telegram-Integration
- Automatische Benachrichtigungen
- Schwellenwert-basierte Warnungen
- Online/Offline-Status von Agenten

### Agent-Komponenten

#### Metriken-Sammlung
- CPU-Auslastung
- Arbeitsspeicher-Nutzung
- Festplatten-Belegung
- System-Temperatur (falls verfügbar)

#### Verbindungsverwaltung
- Automatische Wiederverbindung
- Fehlerbehandlung
- Konfigurierbare Server-URL

## Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Abhängigkeiten
\`\`\`
Flask==2.3.3
Flask-SocketIO==5.3.6
Flask-Login==0.6.3
psutil==5.9.5
python-engineio==4.8.0
python-socketio==5.10.0
python-telegram-bot==20.8
flask-sqlalchemy==3.1.1
werkzeug==3.0.1
python-dotenv==1.0.1
eventlet==0.35.2
\`\`\`

### Installation
1. Repository klonen:
   \`\`\`bash
   git clone https://github.com/riv3ty/monitoring.git
   cd monitoring
   \`\`\`

2. Abhängigkeiten installieren:
   \`\`\`bash
   pip3 install -r requirements.txt
   \`\`\`

3. Umgebungsvariablen konfigurieren:
   \`\`\`bash
   cp .env.example .env
   # .env-Datei bearbeiten und Werte eintragen
   \`\`\`

## Konfiguration

### Umgebungsvariablen (.env)
- \`SECRET_KEY\`: Schlüssel für Flask-Sessions
- \`TELEGRAM_BOT_TOKEN\`: Token für den Telegram-Bot
- \`TELEGRAM_CHAT_ID\`: Chat-ID für Benachrichtigungen

### Schwellenwerte
Standardmäßig sind folgende Schwellenwerte eingestellt:
- CPU: 90%
- Arbeitsspeicher: 90%
- Festplatte: 90%

## Verwendung

### Server starten
\`\`\`bash
python3 server.py
\`\`\`
Der Server läuft standardmäßig auf Port 5011.

### Agent starten
\`\`\`bash
# Lokaler Server
python3 agent.py

# Entfernter Server
python3 agent.py --server http://SERVER_IP:5011

# Test-Modus
python3 agent.py --test
\`\`\`

### Weboberfläche
- URL: http://SERVER_IP:5011
- Registrierung eines neuen Benutzers
- Anmeldung mit Benutzername/Passwort
- Dashboard mit Echtzeit-Metriken

## Technische Details

### Datenmodell

#### User
\`\`\`python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
\`\`\`

#### UserLog
\`\`\`python
class UserLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
\`\`\`

### Metriken-Format
\`\`\`json
{
    "hostname": "server-name",
    "timestamp": 1234567890,
    "cpu_percent": 45.2,
    "memory_percent": 78.5,
    "disk_percent": 65.0,
    "details": {
        "cpu": {
            "frequency": 2500,
            "temperature": 45.0
        },
        "memory": {
            "total": 16.0,
            "used": 12.5
        },
        "disk": {
            "total": 512.0,
            "used": 332.8
        }
    }
}
\`\`\`

## Fehlerbehebung

### Häufige Probleme

#### Server startet nicht
1. Port-Konflikt prüfen:
   \`\`\`bash
   ./kill_processes.sh
   \`\`\`
2. Umgebungsvariablen prüfen
3. Datenbank-Berechtigungen prüfen

#### Agent kann nicht verbinden
1. Server-URL und Port prüfen
2. Firewall-Einstellungen prüfen
3. Socket.IO-Verbindung debuggen:
   \`\`\`python
   # Debug-Logging aktivieren
   self.sio = socketio.Client(logger=True, engineio_logger=True)
   \`\`\`

#### Keine Telegram-Benachrichtigungen
1. Bot-Token prüfen
2. Chat-ID verifizieren
3. Bot-Berechtigungen prüfen

### Logging
- Server-Logs in der Konsole
- Agent-Logs in der Konsole
- Detaillierte Logs bei aktiviertem Debug-Modus

### Sicherheit
- Passwörter werden gehasht gespeichert
- Session-basierte Authentifizierung
- CORS-Schutz aktiviert
- Umgebungsvariablen für sensible Daten

## Detaillierte Code-Dokumentation

### Agent (agent.py)

#### MonitoringAgent Klasse
```python
class MonitoringAgent:
    def __init__(self, server_url='http://localhost:5011', hostname=None, test_mode=False):
        # Initialisierung des Agents mit Server-URL und optionalem Hostnamen
        # test_mode ermöglicht das Testen ohne echte Systemmetriken
```

#### Wichtige Methoden

1. get_metrics()
```python
def get_metrics(self):
    # Sammelt Systemmetriken mit psutil
    # Rückgabe: Dict mit CPU, RAM und Festplatten-Nutzung
    # Beispiel für CPU-Metrik:
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    cpu_freq_current = round(cpu_freq.current, 2) if cpu_freq else None
```

2. run()
```python
def run(self):
    # Hauptmethode zum Starten des Agents
    # - Verbindet sich mit dem Server
    # - Sendet periodisch Metriken
    # - Behandelt Verbindungsfehler
```

### Server (server.py)

#### Flask-Routen

1. Hauptroute
```python
@app.route('/')
@login_required
def index():
    # Rendert das Dashboard
    # Zeigt Metriken aller verbundenen Agenten
```

2. Authentifizierung
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verarbeitet Login-Anfragen
    # Verwendet Flask-Login für Sitzungsverwaltung
```

#### Socket.IO-Events

1. Metriken-Update
```python
@socketio.on('metrics_update')
def handle_metrics_update(data):
    # Empfängt Metriken von Agenten
    # Speichert sie im agents-Dict
    # Sendet Update an alle verbundenen Clients
```

2. Verbindungsmanagement
```python
@socketio.on('connect')
def handle_connect():
    # Behandelt neue Client-Verbindungen
    # Authentifiziert Socket.IO-Clients
```

### Telegram-Notifier (telegram_notifier.py)

```python
class TelegramNotifier:
    def __init__(self, token, chat_id):
        # Initialisiert Bot mit Token
        # Speichert Chat-ID für Nachrichten

    async def send_message(self, message):
        # Sendet formatierte Nachricht
        # Behandelt Fehler beim Senden
```

### Frontend (templates/index.html)

#### Socket.IO-Integration
```javascript
const socket = io({
    transports: ['polling', 'websocket'],
    reconnection: true,
    path: '/socket.io'
});

// Event-Handler für Metriken-Updates
socket.on('metrics_update', function(data) {
    // Aktualisiert UI mit neuen Metriken
    updateMetrics(data.agents);
});
```

#### Metriken-Anzeige
```javascript
function updateMetrics(agents) {
    // Iteriert über alle Agenten
    // Aktualisiert Fortschrittsbalken
    // Zeigt Warnungen bei Überschreitung von Schwellenwerten
}

function getProgressBarClass(percent) {
    // Bestimmt Farbe basierend auf Auslastung
    // < 60%: Grün
    // < 80%: Gelb
    // >= 80%: Rot
}
```

### Datenmodell (models.py)

#### Benutzer-Modell
```python
class User(db.Model, UserMixin):
    # Speichert Benutzerinformationen
    # Implementiert Flask-Login Interface
    # Enthält Methoden für Passwort-Hashing
```

#### Protokollierung
```python
class UserLog(db.Model):
    # Protokolliert Benutzeraktionen
    # Speichert Zeitstempel und durchgeführte Aktionen
```

### Besondere Funktionen

1. Automatische Wiederverbindung
```python
# Im Agent
self.sio.reconnection = True
self.sio.reconnection_attempts = 0  # Unendlich

# Im Frontend
socket.on('disconnect', function() {
    console.log('Verbindung verloren, versuche neu zu verbinden...');
});
```

2. Schwellenwert-Überwachung
```python
def check_thresholds(metrics):
    # Prüft CPU, RAM und Festplatten-Nutzung
    # Sendet Telegram-Benachrichtigung bei Überschreitung
    if metrics['cpu_percent'] > 90:
        notify_telegram(f"Hohe CPU-Auslastung: {metrics['cpu_percent']}%")
```

### Fehlerbehandlung

1. Verbindungsfehler
```python
try:
    self.sio.connect(self.server_url)
except socketio.exceptions.ConnectionError:
    logger.error("Verbindung zum Server fehlgeschlagen")
    time.sleep(5)  # Wartezeit vor erneutem Versuch
```

2. Metriken-Sammlung
```python
try:
    metrics = self.get_metrics()
except Exception as e:
    logger.error(f"Fehler beim Sammeln der Metriken: {e}")
    metrics = self.get_test_metrics()  # Fallback zu Test-Daten
```

### Konfigurationsmanagement

1. Umgebungsvariablen
```python
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
```

2. Kommandozeilenargumente
```python
parser = argparse.ArgumentParser()
parser.add_argument('--server', help='Server URL')
parser.add_argument('--test', action='store_true')
args = parser.parse_args()
```
