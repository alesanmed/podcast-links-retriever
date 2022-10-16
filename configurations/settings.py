import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN") or ""
NAME = os.getenv("BOT_NAME")
WEBHOOK = False
# The following configuration is only needed if you set WEBHOOK to True #
WEBHOOK_OPTIONS = {
    "listen": os.getenv("BOT_IP"),  # IP
    "port": os.getenv("BOT_PORT"),
    "url_path": TOKEN,  # This is recommended for avoiding random people
    # making fake updates to your bot
    "webhook_url": f"{os.getenv('BOT_URL')}/{TOKEN}",
}
