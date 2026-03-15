"""
Test commands.

This plugin provides simple commands used by the automated test
suite. They verify that the command resolver, permission system,
and reply helper work correctly.

Category: test
"""

from utils.command import command, Role


PLUGIN_META = {
    "name": "test",
    "version": "1.0",
    "description": "Testing commands for the bot.",
    "category": "test",
}


@command(
    name="_ping",
    role=Role.OWNER,
)
async def test_ping(bot, sender, nick, args, msg, is_room):
    """
    Test Ping command.

    Responds with "pong". This command is primarily intended for
    automated testing and diagnostics.

    Usage
    -----
    {prefix}ping
    """

    bot.reply(msg, "test pong")
