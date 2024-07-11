from os import makedirs
from os import getenv
import logging
from os.path import exists
from modules.db import UserDatabase
if exists("../.env"):
    from dotenv import load_dotenv
    load_dotenv()


BOT_TOKEN = getenv('BOT_TOKEN')
BOT_USERNAME = getenv('BOT_USERNAME')
TARGET_CHAT_ID = getenv('TARGET_CHAT_ID')
DJANGO_URL = getenv('DJANGO_URL')
REQUEST_MEDIA = 1
ENTER_LAST_NAME = 2
CHANGE_LAST_NAME = 3
MEDIA_FOLDER = 'media_files'
if not exists(MEDIA_FOLDER):
    makedirs(MEDIA_FOLDER)

logger = logging.getLogger(__name__)
db = UserDatabase()
