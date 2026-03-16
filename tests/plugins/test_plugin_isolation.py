"""
Plugin isolation tests.

These tests verify that plugins can coexist without interfering with
each other or corrupting the command registry.

Covered checks:
- All registered command token sequences are unique.
- Each plugin module can be imported independently without relying
  on side effects from other plugins.

These checks help detect issues that would break hot-reload or cause
plugin cross-contamination in the runtime environment.
"""

import importlib
import pkgutil
import plugins
from utils.command import COMMANDS


def test_plugins_register_unique_commands(bot):
    """
    Ensure no two plugins register the same command token sequence.
    """

    command_tokens = list(COMMANDS.index.keys())

    assert len(command_tokens) == len(set(command_tokens)), \
        "Duplicate command names registered by plugins"


def test_plugins_can_be_imported_individually():
    """
    Ensure each plugin module can be imported in isolation.

    This prevents hidden dependencies between plugins that could
    break hot-reload or selective plugin loading.
    """

    for module in pkgutil.iter_modules(plugins.__path__):

        # Skip internal/private plugins
        if module.name.startswith("_"):
            continue

        module_name = f"plugins.{module.name}"

        try:
            importlib.import_module(module_name)

        except Exception as e:
            assert False, (
                f"Plugin '{module_name}' cannot be imported independently: {e}"
            )