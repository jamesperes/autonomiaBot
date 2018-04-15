from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from autonomia.features import dublin_bus


@pytest.mark.vcr
def test_cmd_dublin_bus(bot, update):
    with patch.object(update.message, "reply_text") as m:
        dublin_bus.cmd_dublin_bus(bot, update, args=["1020"])
        m.assert_called_with(
            "Bus stop 1020:\n"
            "    15B - duetime: Due\n"
            "    15 - duetime: 5\n"
            "    14 - duetime: 6\n"
            "    65 - duetime: 9\n"
            "    140 - duetime: 11\n"
        )


def test_cmd_dublin_bus_without_bus_stop(bot, update):
    with patch.object(update.message, "reply_text") as m:
        dublin_bus.cmd_dublin_bus(bot, update, args=[])
        m.assert_called_with("Use: /bus <bus stop number>")


@patch("urllib.request.urlopen")
def test_cmd_dublin_bus_on_error(urlopen_mock, bot, update):
    urlopen_mock.site_effect = ValueError()
    with patch.object(update.message, "reply_text") as m:
        dublin_bus.cmd_dublin_bus(bot, update, args=["1020"])
        m.assert_called_with("To sem saco!")


def test_dublin_bus_factory():
    handler = dublin_bus.dublin_bus_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == dublin_bus.cmd_dublin_bus
    assert handler.command == ["bus"]
    assert handler.pass_args
