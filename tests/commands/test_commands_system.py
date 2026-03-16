"""
Command system validation tests.

These tests verify that commands registered in the command registry
follow the expected structural rules:

- At least one command must exist.
- Command token sequences must be unique.
- Command handlers must be callable.
- Command roles must be valid Role enum values.
- Command handlers must have docstrings.

The tests operate directly on the global command registry.
"""

from utils.command import Role, COMMANDS


def test_commands_registered(bot):
    """Ensure at least one command exists."""

    assert COMMANDS.index, "No commands were registered."


def test_command_names_unique(bot):
    """Ensure command names are unique."""

    names = list(COMMANDS.index.keys())

    assert len(names) == len(set(names)), "Duplicate command names detected."


def test_command_handlers_callable(bot):
    """Ensure command handlers are callable functions."""

    for tokens, cmd in COMMANDS.index.items():

        assert callable(cmd.handler), f"Command '{' '.join(tokens)}' handler is not callable"


def test_command_roles_valid(bot):
    """
    Ensure command roles are valid Role values.
    """

    for tokens, cmd in COMMANDS.index.items():

        role = getattr(cmd, "required_role", Role.NONE)

        assert isinstance(role, Role), f"Command '{' '.join(tokens)}' has invalid role"


def test_command_docstrings(bot):
    """Ensure command handlers have documentation."""

    for tokens, cmd in COMMANDS.index.items():

        doc = cmd.handler.__doc__

        name = " ".join(tokens)

        assert doc is not None, f"Command '{name}' missing docstring"
        assert doc.strip(), f"Command '{name}' has empty docstring"