from importlib import import_module
from logging import getLogger

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher

from connectors.mongodb import get_podcast

logger = getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Busca los enlaces del último capítulo en cada plataforma añadida"""
    dispatcher.add_handler(CommandHandler("enlaces", get_links))


def get_links(update: Update, _: CallbackContext):
    user_id = update.message.from_user.id

    user_podcast = get_podcast(user_id)

    reply_message = ""

    if user_podcast is None:
        reply_message = "No has añadido ninguna plataforma para tu podcast"
    else:
        platforms = user_podcast.platform.keys()

        for platform in platforms:

            module = import_module(f".{platform}", "connectors")

            reply_message += (
                f"{platform.title()}: "
                f"{module.get_last_episode_link(user_podcast.platform[platform])}\n"
            )

    return update.message.reply_text(reply_message, disable_web_page_preview=True)
