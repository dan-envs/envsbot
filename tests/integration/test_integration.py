"""
Integration tests for the bot message handling pipeline.

These tests verify that incoming XMPP messages are routed correctly
through the bot's event handlers and command execution system.

Covered behavior:
- Private messages should trigger command handling.
- Groupchat commands should execute through the normal command handler.
- The bot must ignore its own messages in groupchat environments.
"""

import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_private_message_triggers_command(bot, xmpp_msg):
    """Ensure private messages are forwarded to the command handler."""

    bot.handle_command = AsyncMock()

    xmpp_msg["body"] = ",help"

    await bot.on_private_message(xmpp_msg)

    bot.handle_command.assert_called_once()


@pytest.mark.asyncio
async def test_groupchat_command_execution(bot, xmpp_msg):
    """
    Ensure non-privileged commands execute correctly when received in a groupchat.

    Notes
    -----
    Internal/test commands (plugin filenames starting with "_") are elevated
    to Role.ADMIN by PluginManager. Privileged commands are expected to be
    blocked in groupchat and must be used via direct message instead.
    """

    xmpp_msg["type"] = "groupchat"
    xmpp_msg["body"] = ",status"

    bot._reply_rate = {}

    await bot.handle_command(
        xmpp_msg["body"],
        xmpp_msg["from"].bare,
        "nick",
        xmpp_msg,
        True,
    )

    # "status" replies using bot.reply (so MockMessage.replies is populated)
    assert any("Current status" in r for r in xmpp_msg.replies)


@pytest.mark.asyncio
async def test_bot_does_not_reply_to_itself(bot, xmpp_msg):
    """
    Ensure the bot ignores messages that originate from itself in a MUC.
    """

    xmpp_msg["body"] = ",status"
    xmpp_msg["type"] = "groupchat"

    # Simulate the bot's own nickname in the room
    xmpp_msg["mucnick"] = xmpp_msg["from"].resource
    bot.presence.joined_rooms[xmpp_msg["from"].bare] = xmpp_msg["from"].resource

    await bot.on_muc_message(xmpp_msg)

    assert not xmpp_msg.replies