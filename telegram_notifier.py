import asyncio
from telegram import Bot
from datetime import datetime

class TelegramNotifier:
    def __init__(self, token, chat_id):
        """
        Initialize the TelegramNotifier.
        
        :param token: Telegram Bot API token
        :param chat_id: Chat ID to send messages to
        """
        self.token = token
        self.chat_id = chat_id
        self.bot = Bot(token=token)
        self._device_status = {}  # Track device online status
        print(f"Initialized Telegram notifier with token: {token[:10]}... and chat_id: {chat_id}")
        
    async def send_message(self, message):
        """Send a message via Telegram."""
        try:
            print(f"Sending Telegram message: {message}")
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            print("Message sent successfully")
        except Exception as e:
            print(f"Error sending Telegram message: {e}"
                  f"\nToken: {self.token[:10]}..."
                  f"\nChat ID: {self.chat_id}")

    def format_alert(self, hostname, alert_type, value=None, threshold=None):
        """Format an alert message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"🚨 <b>Alert from {hostname}</b>\n"
        message += f"⏰ Time: {timestamp}\n"
        
        if alert_type == "online":
            message += f"✅ Device is now <b>ONLINE</b>"
        elif alert_type == "offline":
            message += f"❌ Device is now <b>OFFLINE</b>"
        else:
            icon = {
                "ram": "💾",
                "disk": "💿",
                "cpu": "🔄"
            }.get(alert_type, "⚠️")
            
            message += f"{icon} {alert_type.upper()} Usage Alert\n"
            message += f"Current: {value}%\n"
            message += f"Threshold: {threshold}%"
            
        return message

    async def check_thresholds(self, hostname, metrics):
        """
        Check if any metrics exceed their thresholds and send alerts if necessary.
        
        :param hostname: Name of the device
        :param metrics: Dictionary containing device metrics
        """
        alerts = []
        
        # Check if device was previously offline
        if hostname not in self._device_status:
            self._device_status[hostname] = False
            alerts.append(("online", None, None))
        elif not self._device_status[hostname]:
            alerts.append(("online", None, None))
        
        self._device_status[hostname] = True
        
        # Check RAM usage
        memory_percent = (metrics["memory"]["used"] / metrics["memory"]["total"]) * 100
        if memory_percent >= 90:
            alerts.append(("ram", memory_percent, 90))
            
        # Check Disk usage
        disk_percent = (metrics["disk"]["used"] / metrics["disk"]["total"]) * 100
        if disk_percent >= 70:
            alerts.append(("disk", disk_percent, 70))
            
        # Check CPU usage
        if metrics["cpu"]["usage"] >= 80:
            alerts.append(("cpu", metrics["cpu"]["usage"], 80))
            
        # Send alerts
        for alert_type, value, threshold in alerts:
            message = self.format_alert(hostname, alert_type, value, threshold)
            await self.send_message(message)
            
    def mark_offline(self, hostname):
        """Mark a device as offline and send an alert."""
        if hostname in self._device_status and self._device_status[hostname]:
            self._device_status[hostname] = False
            message = self.format_alert(hostname, "offline")
            asyncio.create_task(self.send_message(message))
