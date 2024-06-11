import os
from dotenv import load_dotenv

load_dotenv()

START_PATH = os.getenv('START_PATH', '/default/path')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-100123456789')
DATABASE_URL = os.getenv('DATABASE_URL')
ENDEF_FILES = ['.mp3', '.m4a']
