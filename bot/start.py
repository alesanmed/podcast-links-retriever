# encoding: utf-8

from logging import getLogger

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher

from connectors.mongodb import add_user, user_exists

# Init logger
logger = getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler("start", start))


def start(update: Update, _: CallbackContext):
    """Process a /start command."""    
    user_id = update.message.from_user.id

    if not user_exists(user_id):
        add_user(user_id)

    update.message.reply_text(
        text=(
            "Hola! Soy un bot para pedir todos los links de un nuevo episodio. "
            "Empieza añadiendo una plataforma escribiendo /help"
        )
    )
