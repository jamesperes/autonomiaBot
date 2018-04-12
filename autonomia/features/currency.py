import json
from urllib import request

from telegram.ext import CommandHandler

from autonomia.core import bot_handler
from autonomia.settings import FIXER_IO_API_TOKEN as token

FIXER_IO_API_ENDPOINT = "http://data.fixer.io/api/latest?access_key={0}".format(token)


def cmd_convert(bot, update, args):
    try:
        # laziest ever
        amount, source, target = args
        amount = float(amount)
        source = source.upper()
        target = target.upper()
        req = request.urlopen(request.Request(FIXER_IO_API_ENDPOINT))
        rates = json.loads(req.read())["rates"]

        if source == "EUR":
            result = rates[target] * amount
        elif target == "EUR":
            result = amount / rates[source]
        else:
            partial = amount / rates[source]
            result = rates[target] * float(partial)

        msg = "{0:.2f} {1} is equals to {2:.2f} {3}".format(amount, source, result, target)
        update.message.reply_text(msg)

    except ValueError:
        update.message.reply_text("Errooou! Tenta assim: 10 EUR BRL")
    except KeyError:
        update.message.reply_text("Ta inventando moeda?!")


@bot_handler
def converter_factory():
    """
    /convert - converts a given amount from one currency to another
    """
    return CommandHandler("convert", cmd_convert, pass_args=True)
