from telegram.ext import (ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters,
                          ConversationHandler)
from modules.settings_loader import (BOT_TOKEN, BOT_USERNAME, TARGET_CHAT_ID, DJANGO_URL,
                             REQUEST_MEDIA, ENTER_LAST_NAME, MEDIA_FOLDER, CHANGE_LAST_NAME,
                             logger, db)

from modules.KeyBoard import *
from modules.main_funcs import check_name, check_date

from json import loads
import requests
from time import sleep
from os.path import join
