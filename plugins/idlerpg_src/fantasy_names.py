"""
Fantasy name generation using local static lists with uniqueness enforcement.
Item names are themed to fit their type and rarity.
"""

import random
from .names_lists import (
    NAMES,
    HUMAN_TOWN_NAMES,
    ELVEN_TOWN_NAMES,
    DWARF_TOWN_NAMES,
    DUNGEON_NAMES,
    MOUNTAIN_NAMES,
    FOREST_NAMES,
    ITEM_NAMES,
)

# Track usage counts for uniqueness
_name_usage = {
    "character": {},  # (race, gender): {name: count}
    "town": {},
    "elven_town": {},
    "dwarf_town": {},
    "dungeon": {},
    "mountain": {},
    "forest": {},
    "item": {},
}


def _get_unique_name(name_list, usage_dict):
    counts = usage_dict
    min_count = min([counts.get(n, 0) for n in name_list])
    candidates = [n for n in name_list if counts.get(n, 0) == min_count]
    name = random.choice(candidates)
    counts[name] = counts.get(name, 0) + 1
    return name


def fetch_fantasy_name(race="Human", gender="male"):
    race = race if race in NAMES else "Human"
    gender = gender if gender in NAMES[race] else "male"
    name_list = NAMES[race][gender]
    key = (race, gender)
    if key not in _name_usage["character"]:
        _name_usage["character"][key] = {}
    return _get_unique_name(name_list, _name_usage["character"][key])


def fetch_town_name(race="Human"):
    if race == "Elf":
        arr = ELVEN_TOWN_NAMES
        usage = _name_usage["elven_town"]
    elif race == "Dwarf":
        arr = DWARF_TOWN_NAMES
        usage = _name_usage["dwarf_town"]
    else:
        arr = HUMAN_TOWN_NAMES
        usage = _name_usage["town"]
    return _get_unique_name(arr, usage)


def fetch_dungeon_name():
    return _get_unique_name(DUNGEON_NAMES, _name_usage["dungeon"])


def fetch_mountain_name():
    return _get_unique_name(MOUNTAIN_NAMES, _name_usage["mountain"])


def fetch_forest_name():
    return _get_unique_name(FOREST_NAMES, _name_usage["forest"])


def fetch_item_name(item_type, rarity):
    """
    Generate a unique item name for the given type (e.g. 'staff', 'helmet')
    and rarity.

    Example: 'uncommon Dawnbringer staff'
    """
    # Lowercase rarity for display
    rarity_str = rarity.lower()
    # Use a unique fantasy item name
    if item_type not in _name_usage["item"]:
        _name_usage["item"][item_type] = {}
    base_name = _get_unique_name(ITEM_NAMES, _name_usage["item"][item_type])
    return f"{rarity_str} {base_name} {item_type.lower()}"


def fetch_outdoor_location_name(location_type):
    if location_type == "mountain":
        return fetch_mountain_name()
    elif location_type == "forest":
        return fetch_forest_name()
    else:
        return "Unknown Wilds"
