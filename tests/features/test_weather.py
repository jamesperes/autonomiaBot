from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from autonomia.features import weather


@pytest.mark.vcr
def test_cmd_weather_with_default_value(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = []
        weather.cmd_weather(update, context)
        m.assert_called_with("Dublin, Thu, 12 Apr 2018 07:00 PM IST, 7°C, Cloudy")


@pytest.mark.vcr
def test_cmd_weather_with_args(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["Fortaleza"]
        weather.cmd_weather(update, context)
        m.assert_called_with(
            "Fortaleza, Thu, 12 Apr 2018 03:00 PM BRT, 27°C, Mostly Cloudy"
        )


@patch("autonomia.features.weather._get_weather_info")
def test_cmd_weather_on_error(get_weather_info_mock, update, context):
    get_weather_info_mock.return_value = None
    with patch.object(update.message, "reply_text") as m:
        context.args = []
        assert weather.cmd_weather(update, context) is None
        m.assert_not_called()


def test_weather_factory():
    handler = weather.weather_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == weather.cmd_weather
    assert handler.command == ["weather"]
    assert handler.pass_args
