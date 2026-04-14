"""
Item generation and stats for idleRPG.
Uses d20 SRD 5e as reference for item stats, rarity, value, and usability.
"""

import random
from .fantasy_names import fetch_item_name

RARITY_TABLE = [
    ("Common", 0.7),
    ("Uncommon", 0.2),
    ("Rare", 0.07),
    ("Very Rare", 0.025),
    ("Legendary", 0.005),
]

RARITY_VALUES = {
    "Common": 10,
    "Uncommon": 50,
    "Rare": 250,
    "Very Rare": 2500,
    "Legendary": 25000,
}

# Expanded weapon, armor, and trinket lists with class-based usability only

WEAPON_STATS = [
    {"type": "Longsword", "damage": "1d8", "stat": "STR", "bonus": 0, "classes": ["Fighter", "Paladin", "Barbarian"]},
    {"type": "Greatsword", "damage": "2d6", "stat": "STR", "bonus": 0, "classes": ["Fighter", "Barbarian"]},
    {"type": "Shortsword", "damage": "1d6", "stat": "DEX", "bonus": 0, "classes": ["Rogue", "Fighter", "Monk"]},
    {"type": "Dagger", "damage": "1d4", "stat": "DEX", "bonus": 0, "classes": ["Rogue", "Wizard", "Cleric", "Monk"]},
    {"type": "Battleaxe", "damage": "1d8", "stat": "STR", "bonus": 0, "classes": ["Fighter", "Barbarian", "Druid"]},
    {"type": "Warhammer", "damage": "1d8", "stat": "STR", "bonus": 0, "classes": ["Cleric", "Paladin", "Fighter"]},
    {"type": "Longbow", "damage": "1d8", "stat": "DEX", "bonus": 0, "classes": ["Rogue", "Fighter", "Ranger"]},
    {"type": "Shortbow", "damage": "1d6", "stat": "DEX", "bonus": 0, "classes": ["Rogue", "Monk", "Fighter"]},
    {"type": "Quarterstaff", "damage": "1d6", "stat": "STR", "bonus": 0, "classes": ["Wizard", "Cleric", "Druid", "Monk"]},
    {"type": "Spear", "damage": "1d6", "stat": "STR", "bonus": 0, "classes": ["Druid", "Fighter", "Barbarian"]},
]

ARMOR_STATS = [
    {"type": "Leather Armor", "ac": 11, "classes": ["Rogue", "Monk", "Druid"]},
    {"type": "Chain Mail", "ac": 16, "classes": ["Fighter", "Paladin"]},
    {"type": "Plate Armor", "ac": 18, "classes": ["Fighter", "Paladin"]},
    {"type": "Scale Mail", "ac": 14, "classes": ["Fighter", "Barbarian", "Cleric"]},
    {"type": "Breastplate", "ac": 14, "classes": ["Fighter", "Paladin", "Cleric"]},
    {"type": "Studded Leather Armor", "ac": 12, "classes": ["Rogue", "Bard"]},
    {"type": "Hide Armor", "ac": 12, "classes": ["Barbarian", "Druid"]},
    {"type": "Splint Armor", "ac": 17, "classes": ["Fighter", "Paladin"]},
    {"type": "Ring Mail", "ac": 14, "classes": ["Fighter", "Barbarian"]},
    {"type": "Padded Armor", "ac": 11, "classes": ["Rogue", "Bard"]},
    {"type": "Scale Armor", "ac": 13, "classes": ["Fighter", "Barbarian", "Cleric"]},
]

HELMET_STATS = [
    {"type": "Helmet", "ac": 1, "classes": ["Fighter", "Paladin", "Barbarian", "Cleric"]},
]

GAUNTLETS_STATS = [
    {"type": "Gauntlets", "ac": 1, "classes": ["Fighter", "Paladin", "Barbarian", "Cleric"]},
]

GREAVES_STATS = [
    {"type": "Greaves", "ac": 1, "classes": ["Fighter", "Paladin", "Barbarian", "Cleric"]},
]

TRINKET_STATS = [
    {"type": "Ring", "classes": ["All"]},
    {"type": "Amulet", "classes": ["All"]},
    {"type": "Charm", "classes": ["All"]},
    {"type": "Talisman", "classes": ["All"]},
    {"type": "Brooch", "classes": ["All"]},
    {"type": "Bracelet", "classes": ["All"]},
    {"type": "Medallion", "classes": ["All"]},
    {"type": "Stone", "classes": ["All"]},
]

BONUSES = [
    "Luck", "Charisma", "Wisdom", "Strength", "Dexterity", "Constitution", "Intelligence", "Resist Magic", "Critical", "Double XP"
]


def choose_rarity(bonus_value):
    roll = random.random() * (1 + bonus_value * 0.5)
    cumulative = 0
    for rarity, chance in RARITY_TABLE:
        cumulative += chance
        if roll < cumulative:
            return rarity
    return "Common"


def choose_bonus_and_value(rarity):
    bonus = None
    bonus_value = 0
    roll = random.random()
    if rarity == "Common":
        if roll < 0.1:
            bonus = random.choice(BONUSES)
            bonus_value = random.randint(1, 2)
    elif rarity == "Uncommon":
        if roll < 0.5:
            bonus = random.choice(BONUSES)
            bonus_value = random.randint(1, 3)
    elif rarity == "Rare":
        bonus = random.choice(BONUSES)
        bonus_value = random.randint(2, 4)
    elif rarity == "Very Rare":
        bonus = random.choice(BONUSES)
        bonus_value = random.randint(3, 5)
    elif rarity == "Legendary":
        bonus = random.choice(BONUSES)
        bonus_value = random.randint(4, 6)
    return bonus, bonus_value


def calc_item_value(base_value, rarity, bonus, bonus_value):
    value = base_value * (RARITY_VALUES[rarity] // 10)
    if bonus:
        value += (RARITY_VALUES[rarity] // 2) * bonus_value
    value = int(value * random.uniform(0.8, 1.2))
    return max(value, 1)


def generate_item(item_type):
    """
    Generate an item with a name, stats, rarity, bonus, and gold value.
    """
    if item_type == "weapon":
        base = random.choice(WEAPON_STATS)
        bonus, bonus_value = choose_bonus_and_value("Common")
        rarity = choose_rarity(bonus_value)
        if rarity != "Common":
            bonus, bonus_value = choose_bonus_and_value(rarity)
        name = fetch_item_name(base["type"], rarity)
        item = {
            "name": name,
            "type": base["type"],
            "damage": base["damage"],
            "stat": base["stat"],
            "bonus": base["bonus"],
            "rarity": rarity,
            "usable_classes": base["classes"],
        }
        if bonus:
            item["special"] = f"{bonus} +{bonus_value}"
        item["value"] = calc_item_value(10, rarity, bonus, bonus_value)
    elif item_type == "armor":
        base = random.choice(ARMOR_STATS)
        bonus, bonus_value = choose_bonus_and_value("Common")
        rarity = choose_rarity(bonus_value)
        if rarity != "Common":
            bonus, bonus_value = choose_bonus_and_value(rarity)
        name = fetch_item_name(base["type"], rarity)
        item = {
            "name": name,
            "type": base["type"],
            "ac": base["ac"],
            "rarity": rarity,
            "usable_classes": base["classes"],
        }
        if bonus:
            item["special"] = f"{bonus} +{bonus_value}"
        item["value"] = calc_item_value(10, rarity, bonus, bonus_value)
    elif item_type == "helmet":
        base = random.choice(HELMET_STATS)
        bonus, bonus_value = choose_bonus_and_value("Common")
        rarity = choose_rarity(bonus_value)
        if rarity != "Common":
            bonus, bonus_value = choose_bonus_and_value(rarity)
        name = fetch_item_name(base["type"], rarity)
        item = {
            "name": name,
            "type": base["type"],
            "ac": base["ac"],
            "rarity": rarity,
            "usable_classes": base["classes"],
        }
        if bonus:
            item["special"] = f"{bonus} +{bonus_value}"
        item["value"] = calc_item_value(5, rarity, bonus, bonus_value)
    elif item_type == "gauntlets":
        base = random.choice(GAUNTLETS_STATS)
        bonus, bonus_value = choose_bonus_and_value("Common")
        rarity = choose_rarity(bonus_value)
        if rarity != "Common":
            bonus, bonus_value = choose_bonus_and_value(rarity)
        name = fetch_item_name(base["type"], rarity)
        item = {
            "name": name,
            "type": base["type"],
            "ac": base["ac"],
            "rarity": rarity,
            "usable_classes": base["classes"],
        }
        if bonus:
            item["special"] = f"{bonus} +{bonus_value}"
        item["value"] = calc_item_value(5, rarity, bonus, bonus_value)
    elif item_type == "greaves":
        base = random.choice(GREAVES_STATS)
        bonus, bonus_value = choose_bonus_and_value("Common")
        rarity = choose_rarity(bonus_value)
        if rarity != "Common":
            bonus, bonus_value = choose_bonus_and_value(rarity)
        name = fetch_item_name(base["type"], rarity)
        item = {
            "name": name,
            "type": base["type"],
            "ac": base["ac"],
            "rarity": rarity,
            "usable_classes": base["classes"],
        }
        if bonus:
            item["special"] = f"{bonus} +{bonus_value}"
        item["value"] = calc_item_value(5, rarity, bonus, bonus_value)
    elif item_type == "trinket":
        base = random.choice(TRINKET_STATS)
        bonus, bonus_value = choose_bonus_and_value("Common")
        rarity = choose_rarity(bonus_value)
        if rarity != "Common":
            bonus, bonus_value = choose_bonus_and_value(rarity)
        name = fetch_item_name(base["type"], rarity)
        item = {
            "name": name,
            "type": base["type"],
            "rarity": rarity,
            "usable_classes": base["classes"],
        }
        if bonus:
            item["special"] = f"{bonus} +{bonus_value}"
        item["value"] = calc_item_value(5, rarity, bonus, bonus_value)
    else:
        name = fetch_item_name("Unknown", "Common")
        item = {"name": name, "type": "Unknown", "rarity": "Common", "value": 1, "usable_classes": ["All"]}
    return item
