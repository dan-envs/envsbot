"""
World generation and fantasy name creation for idleRPG.
"""

import random
import logging
import json
import os
import aiofiles
from .fantasy_names import (
    fetch_town_name,
    fetch_dungeon_name,
    fetch_mountain_name,
    fetch_forest_name,
)

WORLD_FILE = "idlerpg_world.json"
WORLD = {}

log = logging.getLogger(__name__)


async def random_level(level_min, level_max):
    weights = [1 / (i + 1) for i in range(level_min, level_max + 1)]
    total = sum(weights)
    weights = [w / total for w in weights]
    return random.choices(range(level_min, level_max + 1), weights=weights)[0]


async def generate_world():
    num_towns = random.randint(4, 10)
    num_mountains = random.randint(3, 6)
    num_forests = random.randint(10, 20)
    num_dungeons = random.randint(30, 50)

    towns = []
    for _ in range(num_towns):
        race = random.choice(["Human", "Elf", "Dwarf"])
        towns.append(
            {"name": fetch_town_name(race), "type": f"{
                race.lower()}_town", "level": 1}
        )

    features = []
    for _ in range(num_mountains):
        features.append({"name": fetch_mountain_name(), "type": "mountain"})
    for _ in range(num_forests):
        features.append({"name": fetch_forest_name(), "type": "forest"})
    for _ in range(num_dungeons):
        features.append({"name": fetch_dungeon_name(), "type": "dungeon"})

    levels_needed = list(range(1, 16))
    random.shuffle(features)
    for i, lvl in enumerate(levels_needed):
        features[i]["level"] = lvl

    for i in range(len(levels_needed), len(features)):
        features[i]["level"] = await random_level(1, 15)

    locations = towns + features
    random.shuffle(locations)

    return {
        "name": fetch_town_name("Human") + " Realm",
        "locations": locations,
        "created": True,
    }


async def save_world():
    async with aiofiles.open(WORLD_FILE, "w") as f:
        await f.write(json.dumps(WORLD))


async def load_world():
    global WORLD
    if os.path.exists(WORLD_FILE):
        async with aiofiles.open(WORLD_FILE, "r") as f:
            data = await f.read()
            WORLD = json.loads(data)
    else:
        WORLD = await generate_world()
        await save_world()


async def on_load(bot):
    global WORLD
    if not WORLD:
        await load_world()
        log.info(f"[IDLERPG]✅ World loaded: {WORLD.get('name')}")
    if not WORLD:
        WORLD = await generate_world()
        await save_world()
        log.info(f"[IDLERPG]✅ World GENERATED: {WORLD.get('name')}")
