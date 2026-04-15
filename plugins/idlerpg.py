"""
idleRPG plugin entry point.

This plugin provides an idle RPG game for XMPP group chats.
It loads submodules for core logic, commands, world, and event handling.
"""
import logging
import asyncio

from utils.command import command, Role
from utils.config import config
from plugins.rooms import JOINED_ROOMS
import slixmpp

from plugins.idlerpg_src.character import get_player, add_xp, save_players
from plugins.idlerpg_src import world, events, character


PLUGIN_META = {
    "name": "idlerpg",
    "version": "0.1.0",
    "description": "Idle RPG game with persistent world and fantasy name generation.",
    "category": "games",
    "requires": ["rooms"],
}

# Setup logging
log = logging.getLogger(__name__)

IDLERPG_ROOM = config.get("idlerpg_room", None)
IDLERPG_EXCLUDED = config.get("idlerpg_excluded", [])
IDLERPG_STATE_KEY = "idlerpg_state"


async def get_user_info(bot, msg):
    room = msg['from'].bare
    nick = msg['from'].resource

    jid = None
    muc = bot.plugin.get("xep_0045", None)
    if muc:
        jid = slixmpp.JID(muc.get_jid_property(
            room, nick, "jid"))
    if jid == "":
        bot.reply(msg, "🔴 Couldn't determine original senders JID")
        log.warning(f"[IDLERPG] 🔴 Couldn't determine original senders JID for room '{room}/{nick}'.")
        return None, None, None, None
    jid = str(slixmpp.JID(jid))

    # is nick in room?
    try:
        nick = dict(JOINED_ROOMS[room]["nicks"][nick])
    except KeyError:
        bot.reply(msg, "🔴 Couldn't determine original senders nick")
        log.warning(f"[IDLERPG] 🔴 Couldn't determine original senders nick for '{jid}': '{room}/{nick}'.")
        return None, None, None, None
    # determine sender role
    user_role = await bot.get_user_role(jid, room)
    return jid, nick, room, user_role


async def get_idlerpg_store(bot):
    return bot.db.users.plugin("idlerpg")


async def get_idlerpg_state(bot):
    store = await get_idlerpg_store(bot)
    state = await store.get_global(IDLERPG_STATE_KEY, default=None)
    if state is None:
        state = {"enabled": False}
        await store.set_global(IDLERPG_STATE_KEY, state)
    return state


async def set_idlerpg_state(bot, enabled):
    store = await get_idlerpg_store(bot)
    state = await get_idlerpg_state(bot)
    state["enabled"] = enabled
    await store.set_global(IDLERPG_STATE_KEY, state)


async def on_load(bot):
    await world.on_load(bot)
    await character.on_load(bot)
    await asyncio.sleep(2)  # Yield to ensure world and character load before events
    await events.on_load(bot)
    # Restore state from PluginRuntimeStore
    if not IDLERPG_ROOM or IDLERPG_ROOM not in JOINED_ROOMS:
        await set_idlerpg_state(bot, False)
    state = await get_idlerpg_state(bot)
    if state.get("enabled"):
        await start_idlerpg(bot, force=True)


async def start_idlerpg(bot, force=False):
    state = await get_idlerpg_state(bot)
    if not world.WORLD:
        await world.load_world()
        log.info(f"[IDLERPG]✅ World loaded: {world.WORLD.get('name')}")
    if not world.WORLD:
        world.WORLD = await world.generate_world()
        await world.save_world()
        log.info(f"[IDLERPG]✅ World GENERATED: {world.WORLD.get('name')}")
    if not character.PLAYERS:
        await character.load_players()
        log.info(f"[IDLERPG]✅ Players loaded!")
    asyncio.sleep(2)  # Yield to ensure world and character load before starting events
    # Only start if not already enabled or if force is True (e.g. after reload)
    if force or not state.get("enabled"):
        await set_idlerpg_state(bot, True)
        # Cancel any existing task to avoid duplicates
        task = getattr(bot, "idlerpg_task", None)
        if task and not task.done():
            task.cancel()
        bot.idlerpg_task = bot.loop.create_task(events.tick_loop(bot))


async def stop_idlerpg(bot):
    state = await get_idlerpg_state(bot)
    if state.get("enabled"):
        await set_idlerpg_state(bot, False)
        task = getattr(bot, "idlerpg_task", None)
        if task:
            task.cancel()
            bot.idlerpg_task = None


@command("idlerpg enable", role=Role.ADMIN)
async def idlerpg_enable(bot, sender_jid, nick, args, msg, is_room):
    """
    Enable idleRPG in this bot instance. Generates a world if needed and starts ticking.
    Usage:
        {prefix}idlerpg enable
    """
    if not IDLERPG_ROOM or IDLERPG_ROOM not in JOINED_ROOMS:
        bot.reply(msg, "🔴 idleRPG room not found!")
        log.warning("[IDLERPG] 🔴 idlerpg_room not configured, cannot enable idleRPG.")
        return
    await start_idlerpg(bot)
    bot.reply(msg, "🟢 idleRPG enabled and world loaded.")
    log.info("[IDLERPG] 🟢 idleRPG enabled and world loaded.")


@command("idlerpg disable", role=Role.ADMIN)
async def idlerpg_disable(bot, sender_jid, nick, args, msg, is_room):
    """
    Disable idleRPG in this bot instance. Stops ticking.
    Usage:
        {prefix}idlerpg disable
    """
    await stop_idlerpg(bot)
    bot.reply(msg, "🔴 idleRPG disabled.")
    log.warning("[IDLERPG] 🔴 idleRPG disabled.")


@command("idlerpg stats", role=Role.USER)
async def idlerpg_stats(bot, sender_jid, nick, args, msg, is_room):
    """
    Show your idleRPG character stats.
    Usage:
        {prefix}idlerpg stats
    """

    if is_room:
        bot.reply(msg, "🔴 Don't write to the Room!")
        return

    # Get user info
    jid, nick, room, user_role = await get_user_info(bot, msg)

    player = await get_player(bot, nick)
    statlines = [f"{k}: {v}" for k, v in player.get("stats", {}).items()]
    things = [inv['name'] for inv in player['inventory']]
    location = player.get("location", "Unknown")
    if "town" in location.get("type"):
        location["type"] = location["type"].replace("_", " ", -1)
    bot.reply(
        msg,
        [
            f"🧙 {player['name']} (Level {player['level']}) {player['race']} {player['class']}",
            f"XP: {player['xp']}/{player['next_level']}, Gold: {player['gold']}",
            f"Location: {location["name"]} ({location["type"]}, level {location['level']})",
            "",
            "- Equipment: -",
            f"Weapon: {player['weapon'].get('name', 'None')}",
            f"Armor: {player['armor'].get('name', 'None')}",
            f"Helmet: {player['helmet'].get('name', 'None')}",
            f"Gloves: {player['gloves'].get('name', 'None')}",
            f"Boots: {player['boots'].get('name', 'None')}",
            f"Rings: {player['ring_left'].get('name', 'None')}, {player['ring_right'].get('name', 'None')}",
            f"Necklace: {player['necklace'].get('name', 'None')}",
            "",
            "- Combat Stats: -",
            f"AC: {player['ac']}, Damage: {player['damage']}, BAB: {player['base_attack_bonus']}",
            f"Hitpoints: {player['hp']}/{player['max_hp']}",
            "",
            "- Abilities: -",
            f"{' | '.join(statlines)}",
            "",
            "- Saves: -",
            f"Fortitude: {player['fort_save']}, Reflex: {player['ref_save']}, Will: {player['will_save']}",
            "- Inventory: ",
            f"{', '.join(things) if things else 'Empty'}"
        ]
    )


@command("idlerpg world", role=Role.USER)
async def idlerpg_world(bot, sender_jid, nick, args, msg, is_room):
    """
    Show info about the idleRPG world.
    Usage:
        {prefix}idlerpg world
    """

    if is_room:
        bot.reply(msg, "🔴 Don't write to the Room!")
        return

    # Get user info
    jid, nick, room, user_role = await get_user_info(bot, msg)

    bot.reply(
        msg,
        [
            f"🌍 World: {world.WORLD['name']}",
            "Locations:",
            *["- " + str(loc) for loc in world.WORLD["locations"]],
        ]
    )


@command("idlerpg idle", role=Role.USER)
async def idlerpg_idle(bot, sender_jid, nick, args, msg, is_room):
    """
    Go idle (simulate inactivity for XP).
    Usage:
        {prefix}idlerpg idle
    """

    if is_room:
        bot.reply(msg, "🔴 Don't write to the Room!")
        return

    # Get user info
    jid, nick, room, user_role = await get_user_info(bot, msg)
    if jid is None:
        bot.reply(msg, "🔴 Could not determine your JID, cannot idle.")
        log.warning(f"[IDLERPG] 🔴 Could not determine JID for '{nick}' in room '{room}', cannot idle.")
        return

    char = await get_player(bot, nick)
    await add_xp(char, 10)
    await save_players()
    bot.reply(msg, f"🛌 {char['name']} idles and gains XP!")


@command("idlerpg help", role=Role.USER)
async def idlerpg_help(bot, sender_jid, nick, args, msg, is_room):
    """
    Show help for idleRPG.
    Usage:
        {prefix}idlerpg help
    """

    if is_room:
        bot.reply(msg, "🔴 Don't write to the Room!")
        return

    # Get user info
    jid, nick, room, user_role = await get_user_info(bot, msg)
    if jid is None:
        bot.reply(msg, "🔴 Could not determine your JID, cannot show help.")
        log.warning(f"[IDLERPG] 🔴 Could not determine JID for '{nick}' in room '{room}', cannot show help.")
        return

    bot.reply(msg, [
        "IdleRPG: Stay idle to gain XP and level up!",
        "Commands: idlerpg stats, idlerpg world, idlerpg idle"
    ])
