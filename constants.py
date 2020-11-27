import os
import json

BOT_TOKEN = os.getenv('BOT_TOKEN', "")
GOOGLE_APPLICATION_CREDENTIALS = json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS', "")) # parse google credentials from json file for service worker
