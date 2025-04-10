# Monitoring System

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