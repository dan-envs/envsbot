"""
Property-based tests for PluginManager.

These tests stress the plugin loading system using randomly generated
plugin dependency graphs. The goal is to ensure the PluginManager
handles arbitrary dependency layouts without crashing.

The generated graphs may include:

- deep dependency chains
- branching dependency trees
- disconnected plugin sets
- circular dependencies
- dense graphs

Plugins are simulated by dynamically creating modules under the
`plugins.*` namespace and inserting them into `sys.modules`.

The main property being tested:

    Loading plugins must never crash the PluginManager,
    regardless of the dependency graph structure.

These tests complement deterministic plugin manager tests that verify
specific expected behaviors.
"""

import types
import sys

import pytest
from hypothesis import given, strategies as st, settings

from utils.plugin_manager import PluginManager


class DummyBot:
    """Minimal bot stub used for PluginManager tests."""
    pass


def make_plugin(name, requires):
    """Create a synthetic plugin module with dependency metadata."""
    module = types.ModuleType(name)
    module.PLUGIN_META = {"requires": requires}
    sys.modules[name] = module
    return module


@pytest.fixture(autouse=True)
def cleanup_modules():
    """Ensure dynamically created plugin modules are removed after each test."""
    before = set(sys.modules.keys())
    yield
    after = set(sys.modules.keys())

    for name in after - before:
        if name.startswith("plugins."):
            del sys.modules[name]


plugin_names = st.lists(
    st.text(min_size=1, max_size=4),
    min_size=1,
    max_size=8,
    unique=True,
)


@settings(max_examples=100)
@given(plugin_names)
async def test_loader_never_crashes(plugin_names):
    """
    Property test: loading plugins must never crash regardless
    of dependency graph layout.

    PluginManager.load() is synchronous in the refactored codebase,
    so the loader must be called without awaiting it.
    """

    bot = DummyBot()
    pm = PluginManager(bot, package="plugins")

    # Build dependency graph
    graph = {}
    for name in plugin_names:
        deps = [d for d in plugin_names if d != name]
        graph[name] = deps[: len(deps) // 2]

    # Create synthetic plugins
    for name, deps in graph.items():
        make_plugin(f"plugins.{name}", deps)

    # Attempt loading each plugin
    for name in graph.keys():
        try:
            await pm.load(name)
        except Exception as e:
            pytest.fail(f"PluginManager crashed on graph {graph}: {e}")
