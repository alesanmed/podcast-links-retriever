from logging import getLogger

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher

from connectors.mongodb import add_platform, add_user, user_exists
from connectors.spotify import get_show_details

logger = getLogger(__name__)


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler("spotify", spotify))


def spotify(update: Update, _: CallbackContext):
    show_id = update.message.text
    user_id = update.message.from_user.id

    reply_message = ""

    try:
        show_details = get_show_details(show_id)

        if not user_exists(user_id):
            add_user(user_id)

        add_platform(user_id, "spotify", show_id)

        reply_message = (
            "Succesfully added Spotify's link for show "
            f"{show_details.name}: {show_details.description}"
        )
    except Exception as exception:
        logger.error(exception)
        reply_message = (
            "There was an error adding your spotify podcast, "
            "please contact the podcast admin"
        )

    update.message.reply_text(reply_message)
