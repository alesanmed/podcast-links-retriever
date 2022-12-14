from logging import getLogger

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher

from connectors.google import get_show_details
from connectors.mongodb import add_platform

logger = getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Añade un podcast desde google podcasts /google url. Ejemplo /google https://podcasts.google.com/feed/aHR0cHM6Ly93d3cuaXZvb3guY29tL2FsZXdhcmUtZW4tZXNwYW5vbF9mZ19mMTkxMTE4Nl9maWx0cm9fMS54bWw"""

    dispatcher.add_handler(CommandHandler("google", google))


def google(update: Update, _: CallbackContext):
    arguments = update.message.text.split(" ")
    user_id = update.message.from_user.id

    reply_message = ""

    if len(arguments) < 2:
        reply_message = (
            "Faltan argumentos, recuerda que tienes que enviar la URL del podcast."
        )

        return update.message.reply_text(reply_message)

    __, show_id = arguments

    try:
        show_details = get_show_details(show_id)

        add_platform(user_id, "google", show_id)

        reply_message = (
            "Añadido correctamente el Podcast\n"
            f"{show_details.name}\n\n"
            f"{show_details.description}"
        )
    except Exception as exception:
        logger.error(exception)
        reply_message = (
            "Hubo un error añadiendo el podcast desde google, "
            "contacta con el admin del bot"
        )

    return update.message.reply_text(reply_message)
