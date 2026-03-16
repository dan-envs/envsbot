"""
Plugin reload integrity tests.

This test verifies that repeatedly reloading plugins does not corrupt the
global command registry.

For every discovered plugin that defines commands, the test checks that:

- command tokens remain identical across reloads
- command ownership remains stable
- command counts remain unchanged
- handler functions are replaced on reload
- plugin module objects change across reloads
- old handler functions become garbage collectible

The global COMMANDS registry is cleared before and after the test to ensure
that other tests or bot initialization cannot contaminate the registry.
"""

import gc
import weakref
import sys

import pytest

from utils.command import COMMANDS

RELOAD_COUNT = 100


def snapshot(plugin):
    """Capture registry state for a plugin."""
    owners = COMMANDS.by_plugin.get(plugin, set())

    handlers = {
        name: COMMANDS.index[name].handler
        for name in owners
    }

    module = sys.modules.get(f"plugins.{plugin}")

    return {
        "command_tokens": set(owners),
        "command_count": len(owners),
        "owners": {name: plugin for name in owners},
        "plugin_handler_count": len(handlers),
        "handler_ids": {name: id(h) for name, h in handlers.items()},
        "module": module,
    }


@pytest.fixture(autouse=True)
def _clean_command_registry():
    """Ensure the global command registry is empty for the test."""
    COMMANDS.index.clear()
    COMMANDS.by_handler.clear()
    COMMANDS.by_plugin.clear()
    COMMANDS.by_prefix.clear()
    yield
    COMMANDS.index.clear()
    COMMANDS.by_handler.clear()
    COMMANDS.by_plugin.clear()
    COMMANDS.by_prefix.clear()


def test_plugin_reload_integrity_all(bot):
    """Repeated plugin reloads must not corrupt the command registry."""

    pm = bot.plugins
    plugins = sorted(pm.discover())

    for plugin in plugins:

        try:
            pm.unload(plugin)
        except Exception:
            pass

        pm.load(plugin)

        before = snapshot(plugin)

        # Skip plugins without commands
        if not before["command_tokens"]:
            continue

        # Capture weakrefs to initial handlers only
        handler_refs = {
            name: weakref.ref(COMMANDS.index[name].handler)
            for name in before["command_tokens"]
        }

        for _ in range(RELOAD_COUNT):

            pm.reload(plugin)

            now = snapshot(plugin)

            assert now["command_tokens"] == before["command_tokens"]
            assert now["command_count"] == before["command_count"]
            assert now["owners"] == before["owners"]
            assert now["plugin_handler_count"] == before["plugin_handler_count"]

            assert now["module"] is not before["module"]
            assert now["handler_ids"] != before["handler_ids"]

        # Drop strong references from snapshot before GC check
        del before
        del now

        gc.collect()

        for ref in handler_refs.values():
            assert ref() is None
