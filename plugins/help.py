def register(bot):

    async def help_command(bot, sender_jid, nick, args, msg, is_room):
        """
        Show help information.

        Usage:
            {prefix}help
            shortcut: {prefix}h
            {prefix}help <command>

        Description:
            Without arguments it lists all commands you are allowed to use.
            When a command name is provided it returns the full help
            documentation for that command.

        Examples:
            {prefix}help
            {prefix}help status
        """

        is_admin = bot.is_admin(sender_jid)

        # destination
        target = msg["from"].bare if is_room else msg["from"]
        mtype = "groupchat" if is_room else "chat"

        # ---- LIST COMMANDS ----
        if not args:

            lines = ["Available commands:"]

            for name, func in sorted(bot.commands.items()):

                if getattr(func, "owner_only", False) and not is_admin:
                    continue

                doc = (func.__doc__ or "").strip().split("\n")[0]

                lines.append(f"{bot.prefix}{name} — {doc}")

            bot.send_message(
                mto=target,
                mbody="\n".join(lines),
                mtype=mtype
            )
            return

        # ---- SHOW COMMAND HELP ----
        cmd = args[0]

        if cmd not in bot.commands:

            bot.send_message(
                mto=target,
                mbody=f"Unknown command: {cmd}",
                mtype=mtype
            )
            return

        func = bot.commands[cmd]

        if getattr(func, "owner_only", False) and not is_admin:

            bot.send_message(
                mto=target,
                mbody="You are not allowed to view this command.",
                mtype=mtype
            )
            return

        doc = func.__doc__ or "No documentation available."

        doc = doc.format(prefix=bot.prefix)

        bot.send_message(
            mto=target,
            mbody=doc.strip(),
            mtype=mtype
        )

    bot.commands["help"] = help_command
    bot.commands["h"] = help_command
