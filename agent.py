import psutil
import platform
import socketio
import time
import argparse
from datetime import datetime

class MonitoringAgent:
    def __init__(self, server_url='http://localhost:5011', hostname=None, test_mode=False):
        self.server_url = server_url
        self.sio = socketio.Client(logger=True, engineio_logger=True)
        self.hostname = hostname or platform.node()
        self.test_mode = test_mode
        
        # Konfiguriere Socket.IO-Client
        self.sio.eio.transports = ['polling', 'websocket']
        self.sio.reconnection = True
        self.sio.reconnection_attempts = 0  # Unendlich
        self.sio.reconnection_delay = 1
        self.sio.reconnection_delay_max = 5

    def get_metrics(self):
        if self.test_mode:
            # Simuliere hohe Auslastung für Tests
            return {
                "hostname": self.hostname,
                "timestamp": int(time.time()),
                "cpu_percent": 95.0,
                "memory_percent": 92.0,
                "disk_percent": 91.0,
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
            "timestamp": int(time.time()),
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent,
            "details": {
                "cpu": {
                    "frequency": cpu_freq_current,
                    "temperature": round(cpu_temp, 2) if cpu_temp else None
                },
                "memory": {
                    "total": round(memory.total / (1024**3), 2),
                    "used": round(memory.used / (1024**3), 2)
                },
                "disk": {
                    "total": round(disk.total / (1024**3), 2),
                    "used": round(disk.used / (1024**3), 2)
                }
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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='System Monitoring Agent')
    parser.add_argument('--server', default='http://localhost:5011',
                      help='Monitoring server URL (default: http://localhost:5011)')
    parser.add_argument('--hostname', help='Custom hostname (default: system hostname)')
    parser.add_argument('--test', action='store_true',
                      help='Run in test mode with simulated high resource usage')
    args = parser.parse_args()

    # Start the agent
    agent = MonitoringAgent(server_url=args.server, hostname=args.hostname, test_mode=args.test)
    agent.run()
