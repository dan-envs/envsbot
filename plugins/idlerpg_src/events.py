"""
idleRPG event handlers.
Handles groupchat events and periodic ticks for the idle RPG game.
"""
import asyncio
import logging
from utils.config import config
from plugins.rooms import JOINED_ROOMS
from .character import get_player, save_players

IDLERPG_ROOM = config.get("idlerpg_room", None)
IDLERPG_EXCLUSION_LIST = config.get("idlerpg_exclusion_list", [])
TICK_INTERVAL = 60  # seconds

log = logging.getLogger(__name__)


async def idle_tick(bot):
    # now = time.time()
    if not IDLERPG_ROOM or IDLERPG_ROOM not in JOINED_ROOMS:
        return
    for jids in JOINED_ROOMS[IDLERPG_ROOM]:
        char = await get_player(jids)
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
