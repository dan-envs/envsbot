"""
Plugin integrity tests.

These tests verify that plugin modules inside the plugins package can
be imported and expose valid metadata required by the plugin system.

Covered checks:
- All public plugin modules can be imported without errors.
- Each plugin exposes a PLUGIN_META dictionary.
- The metadata dictionary contains required fields used by the bot.
"""

import importlib
import pkgutil
import plugins


def _iter_plugin_modules():
    """
    Yield plugin module names, skipping private/internal modules.
    """
    for module in pkgutil.iter_modules(plugins.__path__):
        if module.name.startswith("_"):
            continue
        yield f"plugins.{module.name}"


def test_plugins_importable():
    """
    Ensure all plugin modules can be imported without raising errors.
    """

    for module_name in _iter_plugin_modules():

        try:
            importlib.import_module(module_name)

        except Exception as e:
            assert False, f"Plugin '{module_name}' failed to import: {e}"


def test_plugins_have_metadata():
    """
    Ensure each plugin defines a PLUGIN_META dictionary.
    """

    for module_name in _iter_plugin_modules():

        mod = importlib.import_module(module_name)

        assert hasattr(mod, "PLUGIN_META"), f"{module_name} missing PLUGIN_META"

        meta = mod.PLUGIN_META

        assert isinstance(meta, dict), f"{module_name} PLUGIN_META must be dict"


def test_plugin_metadata_fields():
    """
    Ensure plugin metadata contains required fields.
    """

    required_fields = ["name", "version", "description", "category"]

    for module_name in _iter_plugin_modules():

        mod = importlib.import_module(module_name)

        meta = getattr(mod, "PLUGIN_META", {})

        for field in required_fields:
            assert field in meta, f"{module_name} missing metadata field '{field}'"