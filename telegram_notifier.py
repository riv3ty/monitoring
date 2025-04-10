from telegram import Bot
from telegram.request import HTTPXRequest
import asyncio
import os

class TelegramNotifier:
    def __init__(self, token=None, chat_id=None):
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id_str = chat_id or os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.token or not chat_id_str:
            raise ValueError('Missing Telegram token or chat ID')
            
        try:
            self.chat_id = int(chat_id_str)
            request = HTTPXRequest(connection_pool_size=8)
            self.bot = Bot(token=self.token, request=request)
            print('Telegram bot initialized successfully')
        except ValueError as e:
            raise ValueError(f'Invalid chat ID format: {e}')
        except Exception as e:
            raise Exception(f'Error initializing Telegram bot: {e}')

    async def send_message(self, message):
        if not self.bot:
            raise Exception('Telegram bot not initialized')
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
            print(f'Successfully sent message: {message}')
        except Exception as e:
            print(f'Error sending Telegram message: {e}')
            raise


