# Monitoring System

A real-time system monitoring application built with Python, Flask, and Socket.IO. The system consists of a server component that displays metrics in a web interface and an agent that collects system metrics.

## Features

- Real-time system metrics monitoring
- Web-based dashboard
- Secure login system
- Metrics collected:
  - CPU usage and frequency
  - Memory usage
  - Disk usage
  - System temperature (where available)

## Requirements

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```bash
   python server.py
   ```
   The server will run on port 5011 by default.

2. Start the agent:
   ```bash
   python agent.py
   ```

3. Access the web interface at `http://localhost:5011`

4. Login with the following credentials:
   - Username: `admin`
   - Password: `admin123`

## Configuration

- Server port can be modified in `server.py`
- Agent server URL can be configured in `agent.py`

## Development

The system uses Socket.IO for real-time communication between the server and agent. The web interface updates automatically when new metrics are received.

## Telegram Notifications

The system can send notifications via Telegram when:
- A device comes online
- A device goes offline
- RAM usage exceeds 90%
- Disk usage exceeds 70%
- CPU usage exceeds 80%

### Setting up Telegram Notifications

1. Create a new Telegram bot:
   - Open Telegram and search for @BotFather
   - Send `/newbot` and follow the instructions
   - Save the bot token you receive

2. Get your chat ID:
   - Send a message to your new bot
   - Access `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
   - Look for the `chat` object and note the `id` field

3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file and add your bot token and chat ID:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

5. Restart the server for the changes to take effect

## Übersicht
Dieses Projekt implementiert ein System zur Überwachung von Server-Ressourcen und Systemmetriken. Es besteht aus einem Agent und einem Server-Teil, die zusammenarbeiten, um wichtige Systeminformationen zu sammeln und darzustellen.

## Komponenten

### Agent (agent.py)
- Sammelt Systemmetriken wie CPU-Auslastung, Arbeitsspeichernutzung und Festplattenauslastung
- Sendet regelmäßig Daten an den Server
- Läuft als Hintergrundprozess

### Server (server.py)
- Empfängt Daten von den Agenten
- Stellt eine Weboberfläche zur Visualisierung der Metriken bereit
- Speichert historische Daten

## Installation

1. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## Verwendung

### Server starten
```bash
python server.py
```

### Agent starten
```bash
python agent.py
```

Die Weboberfläche ist dann unter `http://localhost:5000` erreichbar.

## Technische Details
- Python-basierte Implementierung
- Flask für den Webserver
- Echtzeit-Monitoring mit regelmäßigen Updates
- Responsive Weboberfläche für die Darstellung der Metriken