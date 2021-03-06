import json
from unittest.mock import patch

import pytest
from telegram import Update

from autonomia.app import update_webhook


def test_webhook_without_body(flask_client):
    response = flask_client.post("/hook")
    assert response.data == b"fail"


def test_webhook_with_valid_message(telegram_flask_bot, flask_client):
    message = {
        "update_id": 673398956,
        "message": {
            "message_id": 1458,
            "from": {
                "id": 12345,
                "is_bot": False,
                "first_name": "Alan",
                "last_name": "Turing",
                "username": "alanturing",
                "language_code": "en-US",
            },
            "chat": {
                "id": 123456,
                "first_name": "Alan",
                "last_name": "Turing",
                "username": "alanturing",
                "type": "private",
            },
            "date": 1523990402,
            "text": "/help",
            "entities": [{"offset": 0, "length": 5, "type": "bot_command"}],
        },
    }
    update = Update.de_json(message, telegram_flask_bot.bot)
    message = json.dumps(message)
    with patch.object(telegram_flask_bot.dispatcher, "process_update") as m:
        response = flask_client.post(
            "/hook", data=message, content_type="application/json"
        )
        m.assert_called_with(update)
    assert response.data == b"ok"


@pytest.mark.parametrize("updated", [True, False])
@pytest.mark.parametrize(
    "msg",
    [
        "Change webhook to the new url: https://localhost:5000/hook",
        "Unable to get telegram webhook",
    ],
)
def test_update_webhook_cli(telegram_flask_bot, flask_app, updated, msg):
    runner = flask_app.test_cli_runner()
    with patch.object(telegram_flask_bot, "setup_webhook") as m:
        m.return_value = (updated, msg)
        result = runner.invoke(update_webhook)
        assert msg in result.output.strip()
