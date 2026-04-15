"""
idleRPG event handlers.
Handles groupchat events and periodic ticks for the idle RPG game.
"""
import asyncio
import logging
from utils.config import config
from plugins.rooms import JOINED_ROOMS
from .character import get_player, save_players, PLAYERS
from .tools import room_msg

IDLERPG_ROOM = config.get("idlerpg_room", None)
TICK_INTERVAL = 60  # seconds

log = logging.getLogger(__name__)


async def idle_tick(bot):
    # Check if bot is in room
    jids = {nick.get('jid'): nick.get("affiliation") for nick in JOINED_ROOMS[IDLERPG_ROOM]["nicks"].values()}
    if (not IDLERPG_ROOM or IDLERPG_ROOM not in JOINED_ROOMS
            or jids.get(bot.boundjid.bare, None) not in ["owner", "admin"]):
        task = getattr(bot, "idlerpg_task", None)
        if task:
            task.cancel()
            bot.idlerpg_task = None
        log.warning(f"[IDLERPG] No valid room configured for idle RPG. Stopping plugin.")
        return
    nicks = JOINED_ROOMS[IDLERPG_ROOM]["nicks"]
    for nick in nicks:
        if nicks[nick]['jid'] not in config.get("idlerpg_exclude_jids", []):
            char = await get_player(bot, nicks[nick])
            char["active"] = True
    for char in PLAYERS.values():
        if char["nick"]["name"] not in JOINED_ROOMS[IDLERPG_ROOM]["nicks"]:
            char["active"] = False
            char["location"] = char["home"]
            room_msg(bot, [f"🔴 {char["nick"]["name"]} left the room.",
                           (f" {char['name']}, the {char['race']} {char['class']}"
                            " returns home and is inactive.")])

    log.info("[IDLERPG] Ticked!")
    await save_players()


async def tick_loop(bot):
    while True:
        await idle_tick(bot)
        await asyncio.sleep(TICK_INTERVAL)


async def on_load(bot):
    # Start the idle tick loop and store the task on the bot
    bot.idlerpg_task = bot.loop.create_task(tick_loop(bot))
    log.info("[IDLERPG] Tick loop started.")


# Optionally, penalize for talking (reset idle time, etc.)
async def on_groupchat_presence(bot, msg):
    # Example: penalize for sending a message (not implemented)
    pass
