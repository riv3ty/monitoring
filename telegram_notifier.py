from telegram import Bot
import asyncio
import os

class TelegramNotifier:
    def __init__(self, token=None, chat_id=None):
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = int(chat_id or os.getenv('TELEGRAM_CHAT_ID'))
        if self.token and self.chat_id:
            self.bot = Bot(token=self.token)
            # Send startup notification
            asyncio.run(self.send_message('🟢 Monitoring system started'))
        else:
            print('Error: Missing Telegram token or chat ID')
            self.bot = None

    async def send_message(self, message):
        if not self.bot:
            return
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
        except Exception as e:
            print(f"Error sending Telegram message: {e}")

    async def check_thresholds(self, hostname, data):
        if not self.bot:
            return
            
        cpu_percent = data.get('cpu_percent', 0)
        memory_percent = data.get('memory_percent', 0)
        disk_percent = data.get('disk_percent', 0)

        alerts = []
        if cpu_percent > 90:
            alerts.append(f"⚠️ High CPU usage: {cpu_percent}%")
        if memory_percent > 90:
            alerts.append(f"⚠️ High memory usage: {memory_percent}%")
        if disk_percent > 90:
            alerts.append(f"⚠️ High disk usage: {disk_percent}%")

        if alerts:
            message = f"Alert for {hostname}:\n" + "\n".join(alerts)
            await self.send_message(message)
