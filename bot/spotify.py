from logging import getLogger

from pycountry import countries
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher

from connectors.mongodb import add_platform
from connectors.spotify import get_show_details

logger = getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Añade un podcast desde spotify /spotify url CODIGO_PAIS. Ejemplo https://open.spotify.com/show/6PJvg8SvlyGwHK86CuTdFu?si=7deb6832925d4460 ES"""
    dispatcher.add_handler(CommandHandler("spotify", spotify))


def spotify(update: Update, _: CallbackContext):
    arguments = update.message.text.split(" ")
    user_id = update.message.from_user.id

    reply_message = ""

    if len(arguments) < 3:
        reply_message = (
            "Faltan argumentos, recuerda que tienes que enviar el enlace "
            "al podcast y el código del país en el que está publicado"
        )

        return update.message.reply_text(reply_message)

    __, show_id, country = arguments

    if not countries.get(alpha_2=country.upper()):
        reply_message = "El país no es un código de dos dígitos válido"
    else:
        try:
            show_details = get_show_details(show_id, country)

            add_platform(user_id, "spotify", show_id, {"country": country})

            reply_message = (
                "Añadido correctamente el Podcast\n"
                f"{show_details.name}\n\n"
                f"{show_details.description}"
            )
        except Exception as exception:
            logger.error(exception)
            reply_message = (
                "Hubo un error añadiendo el podcast desde spotify, "
                "contacta con el admin del bot"
            )

    return update.message.reply_text(reply_message)
