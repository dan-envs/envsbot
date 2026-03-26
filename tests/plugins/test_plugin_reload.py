"""
Plugin reload safety tests.

These tests verify that loading plugins multiple times does not
duplicate command registrations or corrupt the global command registry.

The command system now uses a global registry (COMMANDS) rather than
storing commands directly on the bot instance, so the tests validate
that the registry contents remain stable across reload operations.
"""

from utils.plugin_manager import PluginManager
from utils.command import COMMANDS


async def test_plugin_reload_does_not_duplicate_commands(bot):
    """
    Ensure reloading plugins does not register duplicate commands.
    """

    pm = bot.plugins

    await pm.load_all()
    initial_commands = set(COMMANDS.index.keys())

    await pm.load_all()
    reloaded_commands = set(COMMANDS.index.keys())

    assert initial_commands == reloaded_commands, \
        "Plugin reload changed command registry"


async def test_plugin_reload_command_count_stable(bot):
    """
    Ensure command count stays stable after plugin reload.
    """

    pm = bot.plugins

    await pm.load_all()
    initial_count = len(COMMANDS.index)

    await pm.load_all()
    reloaded_count = len(COMMANDS.index)

    assert initial_count == reloaded_count, \
        "Plugin reload caused duplicate or missing commands"
