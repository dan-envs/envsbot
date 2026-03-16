"""
Tests for the bot reply helper.

These tests verify that the reply() helper constructs and sends
messages correctly for different message types.

Covered behavior:
- Private chat replies use make_message() and send the message.
- Groupchat replies prefix the message with the sender's nickname
  to create a mention.
"""

from unittest.mock import MagicMock


def test_reply_private(bot, xmpp_msg):
    xmpp_msg["type"] = "chat"

    message = MagicMock()
    bot.make_message.return_value = message

    bot.reply(xmpp_msg, "hello")

    bot.make_message.assert_called_once()
    message.send.assert_called_once()


def test_reply_groupchat_mention(bot, xmpp_msg):
    xmpp_msg["type"] = "groupchat"
    xmpp_msg["mucnick"] = "Alice"

    message = MagicMock()
    bot.make_message.return_value = message

    bot.reply(xmpp_msg, "hello")

    bot.make_message.assert_called_once()

    kwargs = bot.make_message.call_args.kwargs
    assert "Alice:" in kwargs["mbody"]

    message.send.assert_called_once()