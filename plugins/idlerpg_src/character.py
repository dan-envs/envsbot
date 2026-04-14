"""
Character generation for idleRPG using d20 SRD 3.5e rules.
Handles races, classes, stat rolling, modifiers, and unique fantasy names.
"""
import random
import json
import aiofiles
import os
import time
from utils.config import config
from plugins.rooms import JOINED_ROOMS
from .info import CLASS_INFO, RACE_INFO, ITEMS, SKILLS
from .names_lists import NAMES
from . import world
from .tools import room_msg

IDLERPG_ROOM = config.get("idlerpg_room", None)
PLAYERS_FILE = "idlerpg_players.json"
RACES = list(RACE_INFO.keys())
CLASSES = list(CLASS_INFO.keys())
GENDERS = ["male", "female"]
PLAYERS = {}

BASE_STATS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

# Track name usage for uniqueness: {(race, gender): {name: count}}
NAME_USAGE = {}

# d20 SRD 3.5 XP table for levels 1-20 (core rules)
XP_FOR_LEVEL = {
    1: 0,
    2: 1000,
    3: 3000,
    4: 6000,
    5: 10000,
    6: 15000,
    7: 21000,
    8: 28000,
    9: 36000,
    10: 45000,
    11: 55000,
    12: 66000,
    13: 78000,
    14: 91000,
    15: 105000,
    16: 120000,
    17: 136000,
    18: 153000,
    19: 171000,
    20: 190000,
}


def get_name_usage(race, gender):
    key = (race, gender)
    if key not in NAME_USAGE:
        NAME_USAGE[key] = {}
    return NAME_USAGE[key]


def get_unique_name(race, gender):
    name_list = NAMES[race][gender]
    usage = get_name_usage(race, gender)
    min_count = min([usage.get(n, 0) for n in name_list])
    candidates = [n for n in name_list if usage.get(n, 0) == min_count]
    name = random.choice(candidates)
    usage[name] = usage.get(name, 0) + 1
    return name


def roll_stats():
    stats = {}
    for stat in BASE_STATS:
        rolls = sorted([random.randint(1, 6) for _ in range(4)], reverse=True)
        stats[stat] = sum(rolls[:3])
    return stats


def apply_modifiers(stats, mods):
    for k, v in mods.items():
        if k in stats:
            stats[k] += v
    return stats


def get_race_mods(race):
    mods = {}
    for stat, mod in RACE_INFO[race].get("ABILITY_MODIFIERS", {}).items():
        stat_code = stat[:3].upper()
        mods[stat_code] = mod
    return mods


def usable_items_for_class(items, char_class):
    usable = []
    for item in items:
        if "type" in item and "classes" in item:
            if char_class in item["classes"] or "Any" in item["classes"]:
                usable.append(item)
    return usable


async def get_starting_location():
    towns = [loc for loc in world.WORLD.get(
        "locations", []) if "town" in loc.get("type", "")]
    if towns:
        return random.choice(towns)["name"]
    # fallback
    return "Wilderness"


def can_use_shield(char_class, race):
    # Find all shields usable by this class/race
    shields = ITEMS["Shields"]
    class_info = CLASS_INFO[char_class]
    allowed = class_info.get("SHIELDS", [])
    usable = []
    for shield in shields:
        # Normalize shield name for matching
        shield_name = shield["name"].replace("shield (", "").replace(")", "")
        for allowed_name in allowed:
            if allowed_name.replace("shield", "").strip() in shield_name:
                usable.append(shield)
    return usable


def get_class_skills(char_class):
    """Return a set of class skill names for the given class."""
    return set(CLASS_INFO[char_class].get("CLASS_SKILLS", []))


def initialize_skills(char_class):
    """Return a dict of all skills, 1 if class skill, 0 if not."""
    class_skills = get_class_skills(char_class)
    skills = {}
    for skill in SKILLS:
        skills[skill["name"]] = 1 if skill["name"] in class_skills else 0
    return skills


def skill_points_per_level(char_class, int_mod):
    """Calculate skill points per level for the class and INT modifier."""
    base = CLASS_INFO[char_class].get("SKILL_POINTS", 2)
    return max(base + int_mod, 1)


def distribute_skill_points(char, points):
    """Distribute skill points intelligently based on class and current skills."""
    class_skills = get_class_skills(char["class"])
    # Prioritize class skills, especially those with 0 (untrained)
    priorities = []
    for skill in SKILLS:
        name = skill["name"]
        if name in class_skills:
            # Prefer to raise class skills, especially if untrained
            score = 2 if char["skills"][name] == 0 else 1
        else:
            # Only learn non-class skills if points remain
            score = 0.5 if char["skills"][name] == 0 else 0.1
        priorities.append((score, name))
    priorities.sort(reverse=True)
    for _, name in priorities:
        if points <= 0:
            break
        # Max rank = level + 3 for class skill, (level+3)//2 for cross-class
        max_rank = char["level"] + \
            3 if name in class_skills else (char["level"] + 3) // 2
        if char["skills"][name] < max_rank:
            char["skills"][name] += 1
            points -= 1


def get_skill_by_name(skill_name):
    """Return the skill dict from SKILLS by name (case-insensitive)."""
    for skill in SKILLS:
        if skill["name"].lower() == skill_name.lower():
            return skill
    return None


def check_skill(char, skill_name, difficulty):
    """
    Perform a skill check for the given character.
    Returns (success: bool, roll: int, total: int, needed: int)
    """
    skill = get_skill_by_name(skill_name)
    if not skill:
        raise ValueError(f"Unknown skill: {skill_name}")
    # Get ability modifier
    ability = skill["key_ability"]
    stat = char["stats"].get(ability, 10)
    ability_mod = (stat - 10) // 2
    # Skill rank
    rank = char["skills"].get(skill["name"], 0)
    # Armor check penalty
    penalty = 0
    if skill.get("armor_check_penalty", False):
        # If wearing armor, apply penalty (simplified: -2 if any armor)
        if char.get("armor"):
            penalty = -2
    # Untrained?
    if not skill["untrained"] and rank == 0:
        return (False, 0, 0, difficulty)
    roll = random.randint(1, 20)
    total = roll + rank + ability_mod + penalty
    return (total >= difficulty, roll, total, difficulty)


async def generate_character(jid):
    race = random.choice(RACES)
    # 40% chance to use favored class, otherwise random
    if random.random() < 0.4:
        favored_class = RACE_INFO[race].get("FAVORED_CLASS")
        if favored_class and favored_class in CLASSES:
            char_class = favored_class
        else:
            char_class = random.choice(CLASSES)
    else:
        char_class = random.choice(CLASSES)
    gender = random.choice(GENDERS)
    stats = roll_stats()
    stats = apply_modifiers(stats, get_race_mods(race))
    stats = {k: stats.get(k, 0) for k in BASE_STATS}
    name = get_unique_name(race, gender)
    location = await get_starting_location()

    # Weapon
    weapons = usable_items_for_class(ITEMS["Weapons"], char_class)
    weapon = random.choice(weapons) if weapons else None

    # Armor
    armors = usable_items_for_class(ITEMS["Armor"], char_class)
    armor = random.choice(armors) if armors else None

    # Shield (randomly decide to give if usable)
    shields = can_use_shield(char_class, race)
    shield = random.choice(shields) if shields and random.choice(
        [True, False]) else None

    # Calculate max_hp based on class hit die and CON modifier
    # (first level: max)
    class_info = CLASS_INFO[char_class]
    hit_die = class_info.get("HIT_DIE", "d8")
    die_size = int(hit_die[1:])
    con_mod = (stats.get("CON", 10) - 10) // 2
    max_hp = die_size + max(con_mod, 0)
    if max_hp < 1:
        max_hp = 1

    char = {
        "jid": jid,
        "name": name,
        "gender": gender,
        "race": race,
        "class": char_class,
        "level": 1,
        "xp": 0,
        "max_hp": max_hp,
        "hp": max_hp,
        "location": location,
        "weapon": weapon["name"] if weapon else None,
        "armor": armor["name"] if armor else None,
        "shield": shield["name"] if shield else None,
        "helmet": None,
        "gloves": None,
        "boots": None,
        "rings": None,
        "necklace": None,
        "gold": 100,
        "last_action": None,
        "idle_time": 0,
        "stats": stats,
        "saves": {},
    }
    # --- SKILLS ---
    int_mod = (char["stats"].get("INT", 10) - 10) // 2
    char["skills"] = initialize_skills(char["class"])
    # Distribute skill points for level 1
    points = skill_points_per_level(char["class"], int_mod)
    # Humans get +4 at level 1
    if char["race"] == "Human":
        points += 4
    distribute_skill_points(char, points)
    # --- END SKILLS ---
    update_dynamic_stats(char)
    PLAYERS[jid] = char
    return char


def can_level_up(char):
    """Return True if character has enough XP to level up, else False."""
    level = char.get("level", 1)
    xp = char.get("xp", 0)
    next_level = level + 1
    if next_level > 20:
        return False
    xp_needed = XP_FOR_LEVEL.get(next_level)
    if xp_needed is None:
        return False
    return xp >= xp_needed


def calc_base_attack_bonus(char):
    """Calculate BAB for the character's class and level."""
    class_info = CLASS_INFO[char["class"]]
    lvl = char["level"]
    base = class_info.get("BASE", [])
    if lvl <= len(base):
        return base[lvl-1][0]
    return 0


def calc_saves(char):
    """Calculate Fort, Ref, Will saves for class and level."""
    class_info = CLASS_INFO[char["class"]]
    lvl = char["level"]
    fort = class_info.get("FORT_SAVE", [0]*lvl)[lvl-1]
    ref = class_info.get("REF_SAVE", [0]*lvl)[lvl-1]
    will = class_info.get("WILL_SAVE", [0]*lvl)[lvl-1]
    con_mod = (char["stats"].get("CON", 10) - 10) // 2
    dex_mod = (char["stats"].get("DEX", 10) - 10) // 2
    wis_mod = (char["stats"].get("WIS", 10) - 10) // 2
    return {
        "fort_save": fort + con_mod,
        "ref_save": ref + dex_mod,
        "will_save": will + wis_mod,
    }


def calc_ac(char):
    """
    Calculate Armor Class (AC) according to d20 SRD 3.5 rules.
    AC = 10 + DEX mod + armor bonus + shield bonus + size mod + natural armor + deflection + misc + additional_ac
    """
    base_ac = 10
    dex_mod = (char["stats"].get("DEX", 10) - 10) // 2

    # Armor bonus
    armor_bonus = 0
    if char.get("armor"):
        for armor in ITEMS["Armor"]:
            if armor["name"].lower() == str(char["armor"]).lower():
                armor_bonus = armor.get("AC", 0)
                break

    # Shield bonus
    shield_bonus = 0
    if char.get("shield"):
        for shield in ITEMS["Shields"]:
            if shield["name"].lower() == str(char["shield"]).lower():
                shield_bonus = shield.get("AC", 0)
                break

    # Additional AC from Helmets, Gloves, Boots, Rings, Necklace
    additional_ac = 0
    if char.get("helmet"):
        for helmet in ITEMS.get("Helmets", []):
            if helmet["name"].lower() == str(char["helmet"]).lower():
                additional_ac += helmet.get("AC", 0)
                break
    if char.get("gloves"):
        for gloves in ITEMS.get("Gloves", []):
            if gloves["name"].lower() == str(char["gloves"]).lower():
                additional_ac += gloves.get("AC", 0)
                break
    if char.get("boots"):
        for boots in ITEMS.get("Boots", []):
            if boots["name"].lower() == str(char["boots"]).lower():
                additional_ac += boots.get("AC", 0)
                break
    if char.get("rings"):
        for ring in ITEMS.get("Rings", []):
            if ring["name"].lower() == str(char["rings"]).lower():
                additional_ac += ring.get("AC", 0)
                break
    if char.get("necklace"):
        for necklace in ITEMS.get("Necklace", []):
            if necklace["name"].lower() == str(char["necklace"]).lower():
                additional_ac += necklace.get("AC", 0)
                break

    # Size modifier
    size_mod = 0
    size = RACE_INFO[char["race"]].get("SIZE", "Medium")
    size_mods = {"Fine": 8, "Diminutive": 4, "Tiny": 2, "Small": 1,
                 "Medium": 0, "Large": -1, "Huge": -2, "Gargantuan": -4, "Colossal": -8}
    size_mod = size_mods.get(size, 0)

    # Natural armor, deflection, misc (not tracked, set to 0)
    natural_armor = 0
    deflection = 0
    misc = 0

    return base_ac + dex_mod + armor_bonus + shield_bonus + size_mod + natural_armor + deflection + misc + additional_ac


def calc_speed(char):
    """Calculate movement speed."""
    race_info = RACE_INFO[char["race"]]
    return race_info.get("BASE_SPEED", 30)


def update_dynamic_stats(char):
    """Update all dynamic stats for a character."""
    char["ac"] = calc_ac(char)
    char["base_attack_bonus"] = calc_base_attack_bonus(char)
    saves = calc_saves(char)
    char.update(saves)
    char["speed"] = calc_speed(char)


async def add_xp(char, amount):
    char["xp"] += amount
    if can_level_up(char):
        level_up(char)
    return char['xp']


def level_up(char):
    """
    Level up a character according to d20 SRD 3.5 rules.
    - Increase level by 1
    - Roll hit die for class, add CON mod, add to max_hp and hp
    - Update BAB, saves, AC, skill points, feats, etc.
    - Reset XP to 0 or subtract required XP for next level
    - Handle ability score increases at levels 4, 8, 12, 16, 20
    """
    if char["level"] >= 20:
        return  # Max level

    char["level"] += 1

    # Hit Die roll (minimum 1)
    class_info = CLASS_INFO[char["class"]]
    hit_die = class_info.get("HIT_DIE", "d8")
    die_size = int(hit_die[1:])
    con_mod = (char["stats"].get("CON", 10) - 10) // 2
    hp_gain = max(random.randint(1, die_size) + con_mod, 1)
    char["max_hp"] += hp_gain
    char["hp"] += hp_gain

    # Ability score increase every 4th level
    if char["level"] in (4, 8, 12, 16, 20):
        # Choose the stat that gives the best benefit:
        # 1. If any stat is odd, increasing it gives a modifier boost.
        # 2. Prefer primary stat for class (e.g., STR for Fighter, INT for Wizard, etc.)
        # 3. Otherwise, increase the lowest stat.
        def stat_mod(val): return (val - 10) // 2

        primary_stat_by_class = {
            "Fighter": "STR",
            "Barbarian": "STR",
            "Paladin": "STR",
            "Rogue": "DEX",
            "Wizard": "INT",
            "Cleric": "WIS",
            "Druid": "WIS",
            "Monk": "DEX",
            "Sorcerer": "CHA",
            "Bard": "CHA",
            "Ranger": "DEX",
        }
        candidates = [k for k, v in char["stats"].items() if v % 2 == 1]
        primary = primary_stat_by_class.get(char["class"], None)
        if primary and primary in candidates:
            best_stat = primary
        elif candidates:
            best_stat = min(candidates, key=lambda k: char["stats"][k])
        elif primary:
            best_stat = primary
        else:
            best_stat = min(char["stats"], key=lambda k: char["stats"][k])
        char["stats"][best_stat] += 1

    # --- SKILLS ---
    int_mod = (char["stats"].get("INT", 10) - 10) // 2
    points = skill_points_per_level(char["class"], int_mod)
    # Humans get +1 per level
    if char["race"] == "Human":
        points += 1
    distribute_skill_points(char, points)
    # --- END SKILLS ---

    # TODO: new feats, class features, spell slots, etc.
    # These require more detailed implementation per class and +
    # are not included here.

    # Update AC, BAB, saves, speed, etc.
    update_dynamic_stats(char)

    # XP handling: subtract required XP for this level, keep overflow
    xp_needed = XP_FOR_LEVEL[char["level"]]
    if char.get("xp", 0) >= xp_needed:
        char["xp"] -= xp_needed
    else:
        char["xp"] = 0

    # Clamp HP to max_hp
    if char["hp"] > char["max_hp"]:
        char["hp"] = char["max_hp"]


async def create_character(jid):
    char = await generate_character(jid)
    nick = JOINED_ROOMS[IDLERPG_ROOM].get_nick(jid)
    room_msg(
        None,
        f"'{char['name']}', the {char['race']} {char['class']} was created for {nick}.",
        mention=False,
    )
    char["last_action"] = time.time()
    PLAYERS[jid] = char
    await save_players()
    return char


async def get_character(jid):
    if jid not in PLAYERS:
        return await generate_character(jid)
    return PLAYERS[jid]


async def on_load(bot):
    await load_players()
    # Populate NAME_USAGE with actual character names in PLAYERS
    NAME_USAGE.clear()
    for char in PLAYERS.values():
        race = char.get("race")
        gender = char.get("gender")
        name = char.get("name")
        if race and gender and name:
            key = (race, gender)
            if key not in NAME_USAGE:
                NAME_USAGE[key] = {}
            NAME_USAGE[key][name] = NAME_USAGE[key].get(name, 0) + 1


async def save_players():
    async with aiofiles.open(PLAYERS_FILE, "w") as f:
        await f.write(json.dumps(PLAYERS))


async def load_players():
    global PLAYERS
    if os.path.exists(PLAYERS_FILE):
        async with aiofiles.open(PLAYERS_FILE, "r") as f:
            data = await f.read()
            PLAYERS = json.loads(data)
    else:
        PLAYERS = {}


async def get_player(jid):
    if jid not in PLAYERS:
        return await create_character(jid)
    return PLAYERS[jid]
