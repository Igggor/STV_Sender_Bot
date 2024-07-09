from os import getenv
from os.path import exists
if exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()


BOT_TOKEN = getenv('BOT_TOKEN')
BOT_USERNAME = getenv('BOT_USERNAME')
TARGET_CHAT_ID = getenv('TARGET_CHAT_ID')
DJANGO_URL = getenv('DJANGO_URL')
