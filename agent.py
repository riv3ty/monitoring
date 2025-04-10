import psutil
import platform
import socketio
import time
from datetime import datetime

class MonitoringAgent:
    def __init__(self, server_url='http://localhost:5000'):
        self.server_url = server_url
        self.sio = socketio.Client()
        self.hostname = platform.node()

    def get_metrics(self):
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        cpu_temp = None

        # Try to get CPU temperature
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        cpu_temp = entries[0].current
                        break

        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics
        disk = psutil.disk_usage('/')

        return {
            "hostname": self.hostname,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu": {
                "usage": cpu_percent,
                "frequency": round(cpu_freq.current, 2) if cpu_freq else None,
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
        while True:
            try:
                if not self.sio.connected:
                    print(f"Connecting to {self.server_url}...")
                    self.sio.connect(self.server_url)
                    print("Connected!")

                metrics = self.get_metrics()
                print(f"Sending metrics: {metrics}")
                self.sio.emit('metrics_update', metrics)
                time.sleep(2)

            except Exception as e:
                print(f"Error: {str(e)}")
                if self.sio.connected:
                    self.sio.disconnect()
                time.sleep(5)

if __name__ == '__main__':
    agent = MonitoringAgent()
    agent.run()
