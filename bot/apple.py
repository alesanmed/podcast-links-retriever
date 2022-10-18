from logging import getLogger

from pycountry import countries
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher

from connectors.apple import get_show_details
from connectors.mongodb import add_platform

logger = getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Añade un podcast desde apple podcasts /apple codigo CODIGO_PAIS. Ejemplo /apple 1538299550 ES"""
    dispatcher.add_handler(CommandHandler("apple", apple))


def apple(update: Update, _: CallbackContext):
    arguments = update.message.text.split(" ")
    user_id = update.message.from_user.id

    reply_message = ""

    if len(arguments) < 3:
        reply_message = (
            "Faltan argumentos, recuerda que tienes que enviar el id "
            "del podcast y el código del país en el que está publicado"
        )

        return update.message.reply_text(reply_message)

    __, show_id, country = arguments

    if not countries.get(alpha_2=country.upper()):
        reply_message = "El país no es un código de dos dígitos válido"
    if not len(show_id) == 10:
        reply_message = (
            "El código del podcast no parece ser correcto, "
            "debe ser un número parecido a 1538299550"
        )
    else:
        try:
            show_details = get_show_details(show_id, country)

            add_platform(user_id, "apple", show_id, {"country": country})

            reply_message = (
                "Añadido correctamente el Podcast\n"
                f"{show_details.name}\n\n"
                f"{show_details.description}"
            )
        except Exception as exception:
            logger.error(exception)
            reply_message = (
                "Hubo un error añadiendo el podcast desde apple, "
                "contacta con el admin del bot"
            )

    return update.message.reply_text(reply_message)
