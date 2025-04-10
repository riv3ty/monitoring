import psutil
import platform
import socketio
import time
from datetime import datetime

class MonitoringAgent:
    def __init__(self, server_url='http://localhost:5011'):
        self.server_url = server_url
        self.sio = socketio.Client()
        self.hostname = platform.node()

    def get_metrics(self):
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        try:
            cpu_freq = psutil.cpu_freq()
            cpu_freq_current = round(cpu_freq.current, 2) if cpu_freq else None
        except Exception:
            cpu_freq_current = None

        cpu_temp = None
        # Try to get CPU temperature
        if hasattr(psutil, "sensors_temperatures"):
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            cpu_temp = entries[0].current
                            break
            except Exception:
                pass

        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics
        disk = psutil.disk_usage('/')

        return {
            "hostname": self.hostname,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu": {
                "usage": cpu_percent,
                "frequency": cpu_freq_current,
                "temperature": round(cpu_temp, 2) if cpu_temp else None
            },
            "memory": {
                "total": round(memory.total / (1024**3), 2),
                "used": round(memory.used / (1024**3), 2),
                "percent": memory.percent
            },
            "disk": {
                "total": round(disk.total / (1024**3), 2),
                "used": round(disk.used / (1024**3), 2),
                "percent": disk.percent
            }
        }

    def run(self):
        # Setup socket.io event handlers
        @self.sio.event
        def connect():
            print(f"Connected to server at {self.server_url}")

        @self.sio.event
        def connect_error(error):
            print(f"Connection error: {error}")

        @self.sio.event
        def disconnect():
            print("Disconnected from server")

        # Configure socket.io client
        self.sio.reconnection = True
        self.sio.reconnection_attempts = 0  # infinite retries
        self.sio.reconnection_delay = 1
        self.sio.reconnection_delay_max = 5

        # Initial connection
        print(f"Connecting to {self.server_url}...")
        self.sio.connect(self.server_url)

        while True:
            try:
                metrics = self.get_metrics()
                if self.sio.connected:
                    try:
                        self.sio.emit('metrics_update', metrics)
                        print("Metrics sent successfully")
                    except Exception as e:
                        print(f"Error sending metrics: {e}")
                time.sleep(2)

            except Exception as e:
                print(f"Error collecting metrics: {str(e)}")
                time.sleep(5)

if __name__ == '__main__':
    agent = MonitoringAgent()
    agent.run()
