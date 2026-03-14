import importlib
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..")))

import pytest
from unittest.mock import AsyncMock, MagicMock

from tests.xmpp_fixtures import MockMessage
from utils.command import Role


@pytest.fixture
def mock_config(monkeypatch):
    test_config = {
        "jid": "bot@test.local/testbot",
        "password": "test",
        "owner": "owner@test.local",
        "prefix": ",",
        "db": ":memory:"
    }
    # patch the config object used by the bot
    monkeypatch.setattr("utils.config.config", test_config)

    return test_config


@pytest.fixture
def bot(mock_config):

    if "bot" in sys.modules:
        importlib.reload(sys.modules["bot"])

    from bot import Bot

    bot = Bot()

    bot.send_message = MagicMock()
    bot.make_message = MagicMock()

    bot.get_user_role = AsyncMock(return_value=Role.OWNER)
    bot.connect = AsyncMock()

    bot.db.connect = AsyncMock()
    bot.db.close = AsyncMock()

    return bot


@pytest.fixture
def xmpp_msg():
    """
    Provide a realistic mock XMPP message.
    """
    return MockMessage()
