import random
import re
from plugins.rooms import JOINED_ROOMS
from utils.config import config

IDLERPG_ROOM = config.get("idlerpg_room", None)


def roll(dice_str, modifier):
    """
    Roll dice given as "<num>d<sides>" (or "d<sides>") and add modifier.
    Example: "3d6" rolls three six-sided dice, "d20" rolls one twenty-sided
    die. The modifier is added to the result.

    result = roll("3d6", -2)

    Returns the integer result.
    """
    m = re.match(r"^\s*(?:(\d+)?)[dD](\d+)\s*$", dice_str)
    if not m:
        raise ValueError(
            "Invalid dice string format, expected '<num>d<sides>' or 'd<sides>'"
        )
    num = int(m.group(1)) if m.group(1) else 1
    sides = int(m.group(2))
    if num < 1 or sides < 2:
        raise ValueError("Number of dice must be >=1 and sides >=2")
    total = sum(random.randint(1, sides) for _ in range(num))
    return total + modifier


# Utility to send a message to the idleRPG room
def room_msg(bot, text, thread=True, mention=True):
    room = IDLERPG_ROOM
    if not room or room not in JOINED_ROOMS:
        return
    msg_obj = {
        "from": type("F", (), {"bare": room})(),
        "type": "groupchat",
    }
    bot.reply(
        msg_obj,
        text,
        mention=mention,
        thread=thread,
        rate_limit=False,
        ephemeral=False,
    )
