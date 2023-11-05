import os
import telepot
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
# PROXY_URL = "http://proxy.server:3128"  # uncomment to configure
# telepot.api.set_proxy(PROXY_URL)        # pythonanywhere.com proxy
Bot = telepot.Bot(token=API_TOKEN)
SAVE_DIR_NAME = "files"
IMAGES_DIR_NAME = "images"
DOCS_DIR_NAME = "docs"
REQUEST_TIMEOUT = 10
