import os
import telepot
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
BOT = telepot.Bot(token=API_TOKEN)
SAVE_DIR_NAME = "files"
IMAGES_DIR_NAME = "images"
DOCS_DIR_NAME = "docs"
