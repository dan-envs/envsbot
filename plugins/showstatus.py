def register(bot):

    async def showstatus(bot, sender_jid, nick, args, msg, is_room):
        """
        Show the current bot presence status.

        Usage:
            {prefix}status
            {prefix}s

        Description:
            Displays the current presence state of the bot including
            the presence mode and status message.

        Examples:
            {prefix}status
        """

        show = bot.presence.status["show"]
        status = bot.presence.status["status"]
        emoji = bot.presence.emoji()

        target = msg["from"].bare if is_room else msg["from"]

        bot.send_message(
            mto=target,
            mbody=f"Bot status: {emoji} {show} {status}",
            mtype="groupchat" if is_room else "chat"
        )

    bot.commands["status"] = showstatus
    bot.commands["s"] = showstatus
