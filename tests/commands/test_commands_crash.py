"""
Crash-resilience tests for the command system.

This test ensures that every registered command can be executed through the
normal bot command pipeline without raising an unhandled exception.

The permission system is mocked so that all commands run with OWNER
privileges, allowing the test to focus purely on runtime stability rather
than permission enforcement.

Each command is executed twice:
1. As a direct/private message.
2. As a groupchat message.

If any command raises an exception during execution, the test fails and
reports which command caused the crash.
"""

import pytest
from unittest.mock import AsyncMock
from utils.command import Role, COMMANDS


@pytest.mark.asyncio
async def test_commands_do_not_crash(bot, xmpp_msg):

    bot.get_user_role = AsyncMock(return_value=Role.OWNER)

    for tokens in COMMANDS.index:

        name = " ".join(tokens)

        # Direct message test
        xmpp_msg["type"] = "chat"
        xmpp_msg["body"] = f",{name} test"

        try:
            await bot.handle_command(
                xmpp_msg["body"],
                "user@test.local",
                None,
                xmpp_msg,
                False
            )
        except Exception as e:
            pytest.fail(f"Command '{name}' crashed in DM: {e}")

        # Groupchat test
        xmpp_msg["type"] = "groupchat"
        xmpp_msg["body"] = f",{name} test"

        try:
            await bot.handle_command(
                xmpp_msg["body"],
                "user@test.local",
                "nick",
                xmpp_msg,
                False
            )
        except Exception as e:
            pytest.fail(f"Command '{name}' crashed in groupchat: {e}")