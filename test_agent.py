import psutil
import platform
import socketio
import time
from datetime import datetime

class TestAgent:
    def __init__(self, server_url='http://localhost:5011'):
        self.server_url = server_url
        self.sio = socketio.Client()
        self.hostname = "test-system"

    def get_metrics(self):
        return {
            "hostname": self.hostname,
            "timestamp": int(time.time()),
            "cpu_percent": 95.0,  # Simuliere hohe CPU-Auslastung
            "memory_percent": 92.0,  # Simuliere hohen Speicherverbrauch
            "disk_percent": 91.0,  # Simuliere hohe Festplattennutzung
            "details": {
                "cpu": {
                    "frequency": 2500,
                    "temperature": 75.0
                },
                "memory": {
                    "total": 16.0,
                    "used": 14.72
                },
                "disk": {
                    "total": 512.0,
                    "used": 465.92
                }
            }
        }

    def run(self):
        @self.sio.event
        def connect():
            print(f"Connected to server at {self.server_url}")

        @self.sio.event
        def connect_error(error):
            print(f"Connection error: {error}")

        @self.sio.event
        def disconnect():
            print("Disconnected from server")

        self.sio.reconnection = True
        self.sio.reconnection_attempts = 0
        self.sio.reconnection_delay = 1
        self.sio.reconnection_delay_max = 5

        print(f"Connecting to {self.server_url}...")
        self.sio.connect(self.server_url)

        # Sende Metriken für 10 Sekunden
        for _ in range(5):
            try:
                metrics = self.get_metrics()
                if self.sio.connected:
                    self.sio.emit('metrics_update', metrics)
                    print("Metrics sent successfully")
                time.sleep(2)
            except Exception as e:
                print(f"Error: {str(e)}")

        # Beende die Verbindung
        print("Disconnecting...")
        self.sio.disconnect()

if __name__ == '__main__':
    agent = TestAgent()
    agent.run()
