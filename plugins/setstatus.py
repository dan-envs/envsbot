def register(bot):

    async def setstatus(bot, sender_jid, nick, args, msg, is_room):
        """
        Change the bot presence status.

        Usage:
            {prefix}setstatus <show> [status text]
            {prefix},ss <show> [status text]

        Description:
            Updates the bot presence and synchronizes it across all
            joined chat rooms.

        Examples:
            {prefix}setstatus away Getting coffee
            {prefix}setstatus dnd Busy
        """

        target = msg["from"].bare if is_room else msg["from"]
        mtype = "groupchat" if is_room else "chat"

        if not bot.is_admin(sender_jid):
            bot.send_message(mto=target, mbody="Admin only command.", mtype=mtype)
            return

        if not args:
            bot.send_message(
                mto=target,
                mbody=f"Usage: {bot.prefix}setstatus <show> [status]",
                mtype=mtype
            )
            return

        show = args[0]
        status = " ".join(args[1:])

        if show not in bot.presence.emojis:
            bot.send_message(
                mto=target,
                mbody="Invalid presence: online, chat, away, xa, dnd",
                mtype=mtype
            )
            return

        bot.presence.update(show, status)

        emoji = bot.presence.emoji(show)

        bot.send_message(
            mto=target,
            mbody=f"Status updated: {emoji} {show} {status}",
            mtype=mtype
        )

    setstatus.owner_only = True
    bot.commands["setstatus"] = setstatus
    bot.commands["ss"] = setstatus
