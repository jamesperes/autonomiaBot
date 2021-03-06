import datetime
import urllib.parse
from unittest.mock import MagicMock, patch

from telegram.ext import CommandHandler

from autonomia.features import sextou


def test_cmd_sextou_no_arg(update, context, monkeypatch):
    with patch.object(update.message, "reply_text") as m:
        datetime_mock = MagicMock(wraps=datetime.datetime)
        dt = datetime.datetime(2020, 8, 20, 18, 0, 0)
        datetime_mock.now.return_value = dt
        datetime_mock.now.return_value = dt
        monkeypatch.setattr(datetime, "datetime", datetime_mock)
        sextou.cmd_countdown(update, context)
        current_dt = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
        curent_week_day = current_dt.strftime("%A").lower()
        msg = sextou.MESSAGES[curent_week_day]
        m.assert_called_with(
            f"https://www.timeanddate.com/countdown/weekend?iso=20200821T18&p0=78&font=cursive&csz=1&msg={urllib.parse.quote(msg)}"  # noqa
        )


def test_cmd_sextou_messages_friday(update, context, monkeypatch):
    with patch.object(update.message, "reply_text") as m:
        datetime_mock = MagicMock(wraps=datetime.datetime)
        dt = datetime.datetime(2020, 8, 21, 19, 0, 0)
        datetime_mock.now.return_value = dt
        curent_week_day = dt.strftime("%A").lower()
        monkeypatch.setattr(datetime, "datetime", datetime_mock)
        sextou.cmd_countdown(update, context)

        assert sextou.MESSAGES[curent_week_day] == "Ja sinto o cheiro do sextou!"
        m.assert_called_with("Sextou caraiii!")


def test_cmd_sextou_messages_friday_countdown(update, context, monkeypatch):
    with patch.object(update.message, "reply_text") as m:
        datetime_mock = MagicMock(wraps=datetime.datetime)
        dt = datetime.datetime(2020, 8, 21, 14, 0, 0)
        curent_week_day = dt.strftime("%A").lower()
        datetime_mock.now.return_value = dt
        monkeypatch.setattr(datetime, "datetime", datetime_mock)
        sextou.cmd_countdown(update, context)
        assert sextou.MESSAGES[curent_week_day] == "Ja sinto o cheiro do sextou!"
        m.assert_called_with(
            f"https://www.timeanddate.com/countdown/weekend?iso=20200821T18&p0=78&font=cursive&csz=1&msg=Ja%20sinto%20o%20cheiro%20do%20sextou%21"  # noqa
        )


def test_cmd_sextou_messages_weekend_countdown(update, context, monkeypatch):
    with patch.object(update.message, "reply_text") as m:
        datetime_mock = MagicMock(wraps=datetime.datetime)
        dt = datetime.datetime(2020, 8, 22, 14, 0, 0)
        datetime_mock.now.return_value = dt
        curent_week_day = dt.strftime("%A").lower()
        monkeypatch.setattr(datetime, "datetime", datetime_mock)
        assert sextou.MESSAGES[curent_week_day] == "Nao me enche, aproveita o fds"
        sextou.cmd_countdown(update, context)
        m.assert_called_with("Nao me enche, aproveita o fds")

        dt = datetime.datetime(2020, 8, 23, 14, 0, 0)
        datetime_mock.now.return_value = dt
        curent_week_day = dt.strftime("%A").lower()
        monkeypatch.setattr(datetime, "datetime", datetime_mock)
        sextou.cmd_countdown(update, context)

        expected = "Fim de samana acabando, alegria de pobre dura pouco!"
        assert sextou.MESSAGES[curent_week_day] == expected  # noqa
        m.assert_called_with("Fim de samana acabando, alegria de pobre dura pouco!")


def test_cmd_sextou_messages_week_countdown(update, context, monkeypatch):
    with patch.object(update.message, "reply_text") as m:
        datetime_mock = MagicMock(wraps=datetime.datetime)
        dt = datetime.datetime(2020, 8, 20, 14, 0, 0)
        curent_week_day = dt.strftime("%A").lower()
        datetime_mock.now.return_value = dt
        monkeypatch.setattr(datetime, "datetime", datetime_mock)
        sextou.cmd_countdown(update, context)
        assert (
            sextou.MESSAGES[curent_week_day]
            == "A vespera de sexta, Ja vejo o final de semana"  # noqa
        )
        m.assert_called_with(
            f"https://www.timeanddate.com/countdown/weekend?iso=20200821T18&p0=78&font=cursive&csz=1&msg=A%20vespera%20de%20sexta%2C%20Ja%20vejo%20o%20final%20de%20semana"  # noqa
        )


def test_cmd_sextou_messages_monday_countdown(update, context, monkeypatch):
    with patch.object(update.message, "reply_text") as m:
        datetime_mock = MagicMock(wraps=datetime.datetime)

        datetime_mock.now.return_value = datetime.datetime(2020, 8, 17, 14, 0, 0)
        monkeypatch.setattr(datetime, "datetime", datetime_mock)
        sextou.cmd_countdown(update, context)
        m.assert_called_with(
            f"https://www.timeanddate.com/countdown/weekend?iso=20200821T18&p0=78&font=cursive&csz=1&msg=Ta%20longe%20ainda%21"  # noqa
        )


def test_sexout_factory():
    handler = sextou.sexout_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == sextou.cmd_countdown
    assert handler.command == ["sextou"]
