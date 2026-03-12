"""
command.py

Command registration and resolution system for the bot.

This module provides a decorator-based API for registering commands used by
plugins and core bot functionality. It also implements role-based access
control and a hierarchical command resolver that supports multi-word commands
and aliases.

Design goals
------------
- Simple decorator API for plugin authors
- Support hierarchical commands (e.g. "plugins reload")
- Support aliases for commands and tokens
- Resolve the longest matching command
- Provide role-based access control
- Keep implementation self-contained

Role system
-----------
Roles are implemented as an IntEnum with lower numbers representing higher
privileges:

    OWNER      = 1
    ADMIN      = 2
    MODERATOR  = 3
    USER       = 4
    NONE       = 5

Permission rule:
    user_role <= required_role

Examples
--------
Registering commands:
    from bot.command import command, Role

    @command("help")
    async def help_cmd(bot, sender_jid, nick, args, msg, is_room):
        ...

    @command("kick", role=Role.MODERATOR, aliases=["k"])
    async def kick(bot, sender_jid, nick, args, msg, is_room):
        ...

    @command("plugins reload", role=Role.ADMIN,
             aliases=["reload", "pl reload"])
    async def reload_plugins(bot, sender_jid, nick, args, msg, is_room):
        ...

Resolving commands:
    cmd, args = resolve_command("plugins reload test")

    if cmd:
        await cmd.handler(bot, msg, args)

Command resolution
------------------
The resolver performs the following steps:

1. Split the input into tokens
2. Normalize tokens using alias mappings
3. Search for the longest matching command
4. Return the command and remaining tokens as arguments

Example:

    input:  "pl reload pluginA"
    tokens: ["pl", "reload", "pluginA"]

    normalized tokens:
            ["plugins", "reload", "pluginA"]

    matched command:
            "plugins reload"

    args:
            ["pluginA"]
"""

from enum import IntEnum
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


class Role(IntEnum):
    """
    Role hierarchy used for command permission checks.
    Lower numbers represent higher privileges.
    """

    OWNER = 1
    ADMIN = 2
    MODERATOR = 3
    USER = 4
    NONE = 5

    def __str__(self):
        return self.name.lower()


@dataclass
class Command:
    """
    Representation of a registered command.

    Attributes
    ----------
    name:
        Canonical command name (e.g. "plugins reload")
    handler:
        Callable that implements the command
    role:
        Minimum required role to execute the command
    aliases:
        Alternative command names or token aliases
    """

    name: str
    handler: Callable
    role: Role = Role.NONE
    aliases: List[str] = field(default_factory=list)


# Canonical command name -> Command
COMMANDS: Dict[str, Command] = {}

# Token alias -> canonical token
TOKEN_ALIASES: Dict[str, str] = {}


def command(name: str, role: Role = Role.NONE, aliases: Optional[List[str]] = None):
    """
    Decorator used to register a command.

    Parameters
    ----------
    name:
        Canonical command name. May contain multiple words.
    role:
        Minimum role required to execute the command.
    aliases:
        Optional list of alternative command names.

    Examples
    --------
    Basic command:
        @command("help")

    Command with role:
        @command("kick", role=Role.MODERATOR)

    Command with aliases:
        @command("plugins reload",
                 role=Role.ADMIN,
                 aliases=["reload", "pl reload"])
    """

    if aliases is None:
        aliases = []

    def decorator(func: Callable):
        cmd = Command(
            name=name,
            handler=func,
            role=role,
            aliases=aliases
        )
        COMMANDS[name] = cmd

        # register token aliases
        base_tokens = name.split()

        for alias in aliases:
            alias_tokens = alias.split()
            if len(alias_tokens) == len(base_tokens):
                for a, b in zip(alias_tokens, base_tokens):
                    TOKEN_ALIASES[a] = b

        func._command = name
        func._command_names = [name] + aliases
        func._required_role = role
        func._aliases = aliases

        return func

    return decorator


def normalize_tokens(tokens: List[str]) -> List[str]:
    """
    Replace alias tokens with their canonical equivalents.

    Parameters
    ----------
    tokens:
        List of command tokens.

    Returns
    -------
    List[str]
        Normalized tokens.
    """

    normalized = []
    for t in tokens:
        normalized.append(TOKEN_ALIASES.get(t, t))
    return normalized


def resolve_command(text: str):
    """
    Resolve the longest matching command from a text input.

    Parameters
    ----------
    text:
        Command text without the command prefix.

    Returns
    -------
    tuple(Command | None, List[str])
        Command object and argument list.

        If no command is found, the command will be None and the
        tokens will be returned as arguments.
    """

    tokens = text.split()
    tokens = normalize_tokens(tokens)
    best_match = None
    best_length = 0

    for name, cmd in COMMANDS.items():
        cmd_tokens = name.split()

        if len(tokens) < len(cmd_tokens):
            continue

        if tokens[:len(cmd_tokens)] == cmd_tokens:
            if len(cmd_tokens) > best_length:
                best_match = cmd
                best_length = len(cmd_tokens)

    if best_match is None:
        return None, tokens

    args = tokens[best_length:]
    return best_match, args


def has_permission(user_role: Role, required_role: Role) -> bool:
    """
    Check whether a user role satisfies a command's role requirement.

    Parameters
    ----------
    user_role:
        Role of the user executing the command.
    required_role:
        Minimum role required by the command.

    Returns
    -------
    bool
        True if the user may execute the command.
    """

    return user_role <= required_role


def check_permission(user_role: Role, cmd: Command) -> bool:
    """
    Convenience wrapper for permission checking.

    Parameters
    ----------
    user_role:
        Role of the user executing the command.
    cmd:
        Command being executed.

    Returns
    -------
    bool
        True if the user may execute the command.
    """

    return has_permission(user_role, cmd.role)
