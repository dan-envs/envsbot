"""
Help plugin for the bot command system.

Provides an overview of loaded plugins and their commands. Users can
request general help, plugin help, or command help. Command help must
be requested using the configured command prefix so it is not confused
with plugin names.
"""

from command import command, resolve_command

PLUGIN_META = {
    "name": "help",
    "version": "1.0",
    "description": "Show help for plugins and commands.",
    "category": "core",
}


def _first_line(text):
    if not text:
        return ""
    return text.strip().split("\n")[0]


def _clean_doc(doc, prefix):
    if not doc:
        return ""

    lines = []
    for line in doc.strip().splitlines():
        line = line.replace("{prefix}", prefix)
        lines.append(line.strip())

    return "\n".join(lines)


def _commands_for_plugin(bot, plugin_name):
    cmds = []

    for cmd, owner in bot.plugins.command_owner.items():
        if owner == plugin_name:
            fn = bot.commands.get(cmd)
            if fn:
                doc = _first_line(fn.__doc__)
                cmds.append((cmd, doc))

    return sorted(cmds)


@command("help", aliases=["h"])
async def cmd_help(bot, sender_jid, nick, args, msg, is_room):
    """
    Show help.

    Usage:
      {prefix}help
      {prefix}help <plugin>
      {prefix}help {prefix}<command>
    """

    prefix = bot.config.get("prefix", "!")
    pm = bot.plugins
    lines = []

    # normalize args
    if args is None:
        args = []
    elif isinstance(args, str):
        args = args.split()

    # --------------------------------------------------
    # GENERAL HELP
    # --------------------------------------------------

    if not args:
        lines.append("📦 Available plugins:")
        lines.append("")

        for name, module in sorted(pm.plugins.items()):
            doc = _first_line(module.__doc__)
            lines.append(f"• {name} — {doc}")

        lines.append("")
        lines.append(f"Use {prefix}help <plugin> for details.")
        lines.append(f"Use {prefix}help {prefix}<command> for command help.")

    else:
        query = args[0]

        # --------------------------------------------------
        # COMMAND HELP (prefix required)
        # --------------------------------------------------

        if query.startswith(prefix):
            # reconstruct full command string after prefix
            text = " ".join(args)
            text = text[len(prefix):].strip().lower()
            cmd_obj, _ = resolve_command(text)
            if cmd_obj:
                fn = cmd_obj.handler
                doc = _clean_doc(fn.__doc__, prefix)
                lines.append(f"📖 Command: {prefix}{cmd_obj.name}")
                lines.append("")
                if doc:
                    lines.append(doc)
            else:
                lines.append(f"⚠️ Unknown command: {query}")

        # --------------------------------------------------
        # PLUGIN HELP
        # --------------------------------------------------

        else:
            query = query.lower()

            if query in pm.plugins:
                module = pm.plugins[query]

                lines.append(f"📦 Plugin: {query}")
                lines.append("")

                module_doc = _clean_doc(module.__doc__, prefix)
                if module_doc:
                    lines.append(module_doc)
                    lines.append("")

                cmds = _commands_for_plugin(bot, query)

                if cmds:
                    lines.append("Commands:")
                    for name, doc in cmds:
                        lines.append(f"  {prefix}{name} — {doc}")
            else:
                lines.append(f"⚠️ Unknown plugin: {query}")

    bot.reply(msg, "\n".join(lines))
