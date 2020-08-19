from telegram.ext import CommandHandler
from autonomia.core import bot_handler
from dateutil import relativedelta

import urllib.parse
import datetime

BASE_URL = "https://www.timeanddate.com/countdown/weekend"

MESSAGES = {
    'monday': 'Ta longe ainda!',
    'tuesday': 'Ta mais perto, mas ainda eh antevespera da vespera da sexta',
    'wednesday': 'Antevespera ta ai',
    'thursday': 'A vespera de sexta, Ja veo o final de semana',
    'friday': 'Ja sinto o cheiro do sextou!',
    'saturday': 'Nao enche, aproveita o fds',
    'sunday': 'Alegria de pobre dura pouco!'
}


def cmd_countdown(bot, update, args):
    try:
        if "@" in args[0]:
            to = args[0]
            update.message.reply_text(to)

    except IndexError:
        pass

    # Getting current day
    current_dt = datetime.datetime.now().replace(
        tzinfo=datetime.timezone.utc
    )
    curent_week_day = current_dt.strftime("%A").lower()

    # Getting next friday of the week
    friday_rl = relativedelta.relativedelta(days=1, weekday=relativedelta.FR)
    next_friday = current_dt + friday_rl

    # Every friday of the current week at 18
    # This is will be the countdown target
    target_date = next_friday.strftime("%Y%m%dT18")

    user = update.message.from_user.first_name # noqa

    msg = MESSAGES[curent_week_day]
    if curent_week_day == 'saturday' or curent_week_day == 'sunday':
        # If sunday or Saturday just return a single message
        # Enjoy the weekend and leave me alone
        update.message.reply_text(msg)
        return

    if curent_week_day == 'friday' and current_dt.hour >= 18:
        msg = 'Sextou caraiii!'
        update.message.reply_text(msg)
        return

    # Any other day return the countdown
    url = f'{BASE_URL}?iso={target_date}&p0=78&font=cursive&csz=1&msg={urllib.parse.quote(msg)}' # noqa
    update.message.reply_text(url)


@bot_handler
def sexout_factory():
    """
    /sextou? - countdown to friday
    """
    return CommandHandler("sextou", cmd_countdown, pass_args=True)
