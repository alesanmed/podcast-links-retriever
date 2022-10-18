from logging import getLogger

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher

from connectors.ivoox import get_show_details
from connectors.mongodb import add_platform

logger = getLogger(__name__)


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler("ivoox", ivoox))


def ivoox(update: Update, _: CallbackContext):
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

        add_platform(user_id, "ivoox", show_id)

        reply_message = (
            "Añadido correctamente el Podcast\n"
            f"{show_details.name}\n\n"
            f"{show_details.description}"
        )
    except Exception as exception:
        logger.error(exception)
        reply_message = (
            "Hubo un error añadiendo el podcast desde ivoox, "
            "contacta con el admin del bot"
        )

    return update.message.reply_text(reply_message)
