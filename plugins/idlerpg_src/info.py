# All possible alignments
ALIGNMENTS = [
    "Lawful Good",
    "Neutral Good",
    "Chaotic Good",
    "Lawful Neutral",
    "True Neutral",
    "Chaotic Neutral",
    "Lawful Evil",
    "Neutral Evil",
    "Chaotic Evil"
]

# d20 SRD 3.5e class information for all core classe
CLASS_INFO = {
    "Barbarian": {
        "HIT_DIE": "d12",
        "ALIGNMENT": [
            "Chaotic Good", "Neutral Good", "Chaotic Neutral", "True Neutral",
            "Neutral Evil", "Chaotic Evil"
        ],
        "SKILL_POINTS": 4,
        "CLASS_SKILLS": [
            "Climb", "Craft", "Handle Animal", "Intimidate", "Jump", "Listen",
            "Ride", "Survival", "Swim"
        ],
        "WEAPONS": ["simple", "martial"],
        "ARMOR": ["light", "medium"],
        "SHIELDS": [
            "buckler", "light shield", "heavy shield"
        ],
        "SPECIAL_ABILITIES": {
            1: ["Fast Movement", "Illiteracy", "Rage 1/day"],
            2: ["Uncanny Dodge"],
            3: ["Trap Sense +1"],
            5: ["Improved Uncanny Dodge"],
            7: ["Damage Reduction 1/-"],
            11: ["Greater Rage"],
            15: ["Indomitable Will"],
            17: ["Tireless Rage"],
            20: ["Mighty Rage"],
        },
        "BASE": [
            [1], [2], [3], [4], [5], [6, 1], [7, 2], [8, 3], [9, 4], [10, 5],
            [11, 6, 1], [12, 7, 2], [13, 8, 3], [14, 9, 4], [15, 10, 5],
            [16, 11, 6, 1], [17, 12, 7, 2], [18, 13, 8, 3], [19, 14, 9, 4], [20, 15, 10, 5]
        ],
        "FORT_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "REF_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "WILL_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    },
    "Fighter": {
        "HIT_DIE": "d10",
        "ALIGNMENT": ["Any"],
        "SKILL_POINTS": 2,
        "CLASS_SKILLS": [
            "Climb", "Craft", "Handle Animal", "Intimidate", "Jump", "Ride", "Swim"
        ],
        "WEAPONS": ["simple", "martial"],
        "ARMOR": ["light", "medium", "heavy"],
        "SHIELDS": [
            "buckler", "light shield", "heavy shield", "tower shield"
        ],
        "SPECIAL_ABILITIES": {
            1: ["Bonus Feat"],
            2: ["Bonus Feat"],
            4: ["Bonus Feat"],
            6: ["Bonus Feat"],
            8: ["Bonus Feat"],
            10: ["Bonus Feat"],
            12: ["Bonus Feat"],
            14: ["Bonus Feat"],
            16: ["Bonus Feat"],
            18: ["Bonus Feat"],
            20: ["Bonus Feat"],
        },
        "BASE": [
            [1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
            [11], [12], [13], [14], [15], [16], [17], [18], [19], [20]
        ],
        "FORT_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "REF_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "WILL_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    },
    "Paladin": {
        "HIT_DIE": "d10",
        "ALIGNMENT": ["Lawful Good"],
        "SKILL_POINTS": 2,
        "CLASS_SKILLS": [
            "Concentration", "Craft", "Diplomacy", "Handle Animal", "Heal",
            "Knowledge (nobility and royalty)", "Knowledge (religion)", "Profession",
            "Ride", "Sense Motive"
        ],
        "WEAPONS": ["simple", "martial"],
        "ARMOR": ["light", "medium", "heavy"],
        "SHIELDS": [
            "buckler", "light shield", "heavy shield", "tower shield"
        ],
        "SPECIAL_ABILITIES": {
            1: ["Aura of Good", "Detect Evil", "Smite Evil 1/day"],
            2: ["Divine Grace", "Lay on Hands"],
            3: ["Divine Health"],
            4: ["Turn Undead"],
            5: ["Smite Evil 2/day", "Special Mount"],
            6: ["Remove Disease 1/week"],
            9: ["Remove Disease 2/week"],
            12: ["Remove Disease 3/week"],
            15: ["Remove Disease 4/week"],
            18: ["Remove Disease 5/week"],
            20: ["Smite Evil 4/day"],
        },
        "BASE": [
            [1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
            [11], [12], [13], [14], [15], [16], [17], [18], [19], [20]
        ],
        "FORT_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "REF_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "WILL_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "SPELLS_PER_DAY": {
            1: [0, 0, 0, 0],
            2: [0, 0, 0, 0],
            3: [0, 0, 0, 0],
            4: [0, 0, 0, 0],
            5: [1, 0, 0, 0],
            6: [1, 0, 0, 0],
            7: [1, 0, 0, 0],
            8: [1, 1, 0, 0],
            9: [1, 1, 0, 0],
            10: [1, 1, 0, 0],
            11: [1, 1, 1, 0],
            12: [1, 1, 1, 0],
            13: [1, 1, 1, 1],
            14: [1, 1, 1, 1],
            15: [2, 1, 1, 1],
            16: [2, 1, 1, 1],
            17: [2, 2, 1, 1],
            18: [2, 2, 1, 1],
            19: [2, 2, 2, 1],
            20: [2, 2, 2, 2],
        }
    },
    "Rogue": {
        "HIT_DIE": "d6",
        "ALIGNMENT": ["Any"],
        "SKILL_POINTS": 8,
        "CLASS_SKILLS": [
            "Appraise", "Balance", "Bluff", "Climb", "Craft", "Decipher Script", "Diplomacy",
            "Disable Device", "Disguise", "Escape Artist", "Forgery", "Gather Information", "Hide",
            "Intimidate", "Jump", "Knowledge (local)", "Listen", "Move Silently", "Open Lock",
            "Perform", "Profession", "Search", "Sense Motive", "Sleight of Hand", "Spot", "Swim",
            "Tumble", "Use Magic Device", "Use Rope"
        ],
        "WEAPONS": [
            "simple", "hand crossbow", "rapier", "sap", "shortbow", "shortsword"
        ],
        "ARMOR": ["light"],
        "SHIELDS": [],
        "SPECIAL_ABILITIES": {
            1: ["Sneak Attack +1d6", "Trapfinding"],
            2: ["Evasion"],
            3: ["Trap Sense +1"],
            4: ["Uncanny Dodge"],
            5: ["Sneak Attack +3d6"],
            8: ["Improved Uncanny Dodge"],
            10: ["Special Ability"],
            13: ["Special Ability"],
            16: ["Special Ability"],
            19: ["Special Ability"],
        },
        "BASE": [
            [0], [1], [2], [3], [3, 1], [4, 1], [5, 2], [6, 2], [6, 3], [7, 3],
            [8, 4, 1], [9, 4, 2], [9, 5, 2], [10, 5, 3], [11, 6, 3], [12, 6, 4],
            [12, 7, 4], [13, 7, 5], [14, 8, 5], [14, 9, 6]
        ],
        "FORT_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "REF_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "WILL_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    },
    "Wizard": {
        "HIT_DIE": "d4",
        "ALIGNMENT": ["Any"],
        "SKILL_POINTS": 2,
        "CLASS_SKILLS": [
            "Concentration", "Craft", "Decipher Script", "Knowledge (all)", "Profession", "Spellcraft"
        ],
        "WEAPONS": [
            "club", "dagger", "heavy crossbow", "light crossbow", "quarterstaff"
        ],
        "ARMOR": [],
        "SHIELDS": [],
        "SPECIAL_ABILITIES": {
            1: ["Summon Familiar", "Scribe Scroll"],
            5: ["Bonus Feat"],
            10: ["Bonus Feat"],
            15: ["Bonus Feat"],
            20: ["Bonus Feat"],
        },
        "BASE": [
            [0], [1], [1], [2], [2], [3], [3], [4], [4], [5],
            [5], [6], [6], [7], [7], [8], [8], [9], [9], [10]
        ],
        "FORT_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "REF_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "WILL_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "SPELLS_PER_DAY": {
            1: [3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            2: [4, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            3: [4, 2, 1, 0, 0, 0, 0, 0, 0, 0],
            4: [4, 3, 2, 0, 0, 0, 0, 0, 0, 0],
            5: [4, 3, 2, 1, 0, 0, 0, 0, 0, 0],
            6: [4, 3, 3, 2, 0, 0, 0, 0, 0, 0],
            7: [4, 4, 3, 2, 1, 0, 0, 0, 0, 0],
            8: [4, 4, 3, 3, 2, 0, 0, 0, 0, 0],
            9: [4, 4, 4, 3, 2, 1, 0, 0, 0, 0],
            10: [4, 4, 4, 3, 3, 2, 0, 0, 0, 0],
            11: [4, 4, 4, 4, 3, 2, 1, 0, 0, 0],
            12: [4, 4, 4, 4, 3, 3, 2, 0, 0, 0],
            13: [4, 4, 4, 4, 4, 3, 2, 1, 0, 0],
            14: [4, 4, 4, 4, 4, 3, 3, 2, 0, 0],
            15: [4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
            16: [4, 4, 4, 4, 4, 4, 3, 3, 2, 0],
            17: [4, 4, 4, 4, 4, 4, 4, 3, 2, 1],
            18: [4, 4, 4, 4, 4, 4, 4, 3, 3, 2],
            19: [4, 4, 4, 4, 4, 4, 4, 4, 3, 3],
            20: [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        }
    },
    "Cleric": {
        "HIT_DIE": "d8",
        "ALIGNMENT": ["Any"],
        "SKILL_POINTS": 2,
        "CLASS_SKILLS": [
            "Concentration", "Craft", "Diplomacy", "Heal", "Knowledge (arcana)", "Knowledge (history)",
            "Knowledge (religion)", "Knowledge (the planes)", "Profession", "Spellcraft"
        ],
        "WEAPONS": ["simple"],
        "ARMOR": ["light", "medium", "heavy"],
        "SHIELDS": [
            "buckler", "light shield", "heavy shield", "tower shield"
        ],
        "SPECIAL_ABILITIES": {
            1: ["Turn Undead", "Spontaneous Casting"],
            5: ["Bonus Feat"],
            10: ["Bonus Feat"],
            15: ["Bonus Feat"],
            20: ["Bonus Feat"],
        },
        "BASE": [
            [0], [1], [2], [3], [3], [4], [5], [6], [6], [7],
            [8], [9], [9], [10], [11], [12], [12], [13], [14], [14]
        ],
        "FORT_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "REF_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "WILL_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "SPELLS_PER_DAY": {
            1: [3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            2: [4, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            3: [4, 2, 1, 0, 0, 0, 0, 0, 0, 0],
            4: [4, 3, 2, 0, 0, 0, 0, 0, 0, 0],
            5: [4, 3, 2, 1, 0, 0, 0, 0, 0, 0],
            6: [4, 3, 3, 2, 0, 0, 0, 0, 0, 0],
            7: [4, 4, 3, 2, 1, 0, 0, 0, 0, 0],
            8: [4, 4, 3, 3, 2, 0, 0, 0, 0, 0],
            9: [4, 4, 4, 3, 2, 1, 0, 0, 0, 0],
            10: [4, 4, 4, 3, 3, 2, 0, 0, 0, 0],
            11: [4, 4, 4, 4, 3, 2, 1, 0, 0, 0],
            12: [4, 4, 4, 4, 3, 3, 2, 0, 0, 0],
            13: [4, 4, 4, 4, 4, 3, 2, 1, 0, 0],
            14: [4, 4, 4, 4, 4, 3, 3, 2, 0, 0],
            15: [4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
            16: [4, 4, 4, 4, 4, 4, 3, 3, 2, 0],
            17: [4, 4, 4, 4, 4, 4, 4, 3, 2, 1],
            18: [4, 4, 4, 4, 4, 4, 4, 3, 3, 2],
            19: [4, 4, 4, 4, 4, 4, 4, 4, 3, 3],
            20: [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        }
    },
    "Monk": {
        "HIT_DIE": "d8",
        "ALIGNMENT": [
            "Lawful Good", "Lawful Neutral", "Lawful Evil"
        ],
        "SKILL_POINTS": 4,
        "CLASS_SKILLS": [
            "Balance", "Climb", "Concentration", "Craft", "Diplomacy", "Escape Artist", "Hide",
            "Jump", "Knowledge (arcana)", "Listen", "Move Silently", "Perform", "Profession",
            "Sense Motive", "Spot", "Swim", "Tumble"
        ],
        "WEAPONS": [
            "club", "crossbow (light)", "dagger", "handaxe", "javelin", "kama", "nunchaku",
            "quarterstaff", "sai", "shuriken", "siangham", "sling", "short sword"
        ],
        "ARMOR": [],
        "SHIELDS": [],
        "UNARMED_DAMAGE": {
            1: ["1d4", "1d6", "1d8"],
            4: ["1d6", "1d8", "2d6"],
            8: ["1d8", "1d10", "2d8"],
            12: ["1d10", "2d6", "3d6"],
            16: ["2d6", "2d8", "3d8"],
            20: ["2d8", "2d10", "4d8"],
        },
        "AC_BONUS": {
            1: 0,
            4: 1,
            9: 2,
            14: 3,
            19: 4,
        },
        "SPECIAL_ABILITIES": {
            1: ["Flurry of Blows", "Unarmed Strike", "Bonus Feat", "AC Bonus"],
            2: ["Evasion"],
            3: ["Still Mind"],
            4: ["Ki Strike (magic)", "Slow Fall 20 ft."],
            5: ["Purity of Body"],
            6: ["Bonus Feat"],
            7: ["Wholeness of Body"],
            9: ["Improved Evasion"],
            10: ["Ki Strike (lawful)", "Slow Fall 50 ft."],
            11: ["Diamond Body"],
            12: ["Abundant Step"],
            13: ["Diamond Soul"],
            15: ["Quivering Palm"],
            17: ["Timeless Body", "Tongue of the Sun and Moon"],
            18: ["Empty Body"],
            19: ["Perfect Self"],
        },
        "BASE": [
            [0], [1], [2], [3], [3, 1], [4, 1], [5, 2], [6, 2], [6, 3], [7, 3],
            [8, 4, 1], [9, 4, 2], [9, 5, 2], [10, 5, 3], [11, 6, 3], [12, 6, 4],
            [12, 7, 4], [13, 7, 5], [14, 8, 5], [14, 9, 6]
        ],
        "FORT_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "REF_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "WILL_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
    },
    "Druid": {
        "HIT_DIE": "d8",
        "ALIGNMENT": [
            "Neutral", "Neutral Good", "Neutral Evil", "Lawful Neutral", "Chaotic Neutral"
        ],
        "SKILL_POINTS": 4,
        "CLASS_SKILLS": [
            "Concentration", "Craft", "Diplomacy", "Handle Animal", "Heal", "Knowledge (nature)",
            "Listen", "Profession", "Ride", "Spellcraft", "Spot", "Survival", "Swim"
        ],
        "WEAPONS": [
            "club", "dagger", "dart", "quarterstaff", "scimitar", "sickle", "shortspear", "sling", "spear"
        ],
        "ARMOR": ["light (nonmetal)", "medium (nonmetal)"],
        "SHIELDS": ["buckler (nonmetal)", "light shield (nonmetal)", "heavy shield (nonmetal)"],
        "SPECIAL_ABILITIES": {
            1: ["Nature Sense", "Wild Empathy"],
            2: ["Woodland Stride"],
            3: ["Trackless Step"],
            4: ["Resist Nature's Lure"],
            5: ["Wild Shape 1/day"],
            9: ["Venom Immunity"],
            13: ["A Thousand Faces"],
            15: ["Timeless Body"],
        },
        "BASE": [
            [0], [1], [2], [3], [3], [4], [5], [6], [6], [7],
            [8], [9], [9], [10], [11], [12], [12], [13], [14], [14]
        ],
        "FORT_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "REF_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "WILL_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "SPELLS_PER_DAY": {
            1: [3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            2: [4, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            3: [4, 2, 1, 0, 0, 0, 0, 0, 0, 0],
            4: [4, 3, 2, 0, 0, 0, 0, 0, 0, 0],
            5: [4, 3, 2, 1, 0, 0, 0, 0, 0, 0],
            6: [4, 3, 3, 2, 0, 0, 0, 0, 0, 0],
            7: [4, 4, 3, 2, 1, 0, 0, 0, 0, 0],
            8: [4, 4, 3, 3, 2, 0, 0, 0, 0, 0],
            9: [4, 4, 4, 3, 2, 1, 0, 0, 0, 0],
            10: [4, 4, 4, 3, 3, 2, 0, 0, 0, 0],
            11: [4, 4, 4, 4, 3, 2, 1, 0, 0, 0],
            12: [4, 4, 4, 4, 3, 3, 2, 0, 0, 0],
            13: [4, 4, 4, 4, 4, 3, 2, 1, 0, 0],
            14: [4, 4, 4, 4, 4, 3, 3, 2, 0, 0],
            15: [4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
            16: [4, 4, 4, 4, 4, 4, 3, 3, 2, 0],
            17: [4, 4, 4, 4, 4, 4, 4, 3, 2, 1],
            18: [4, 4, 4, 4, 4, 4, 4, 3, 3, 2],
            19: [4, 4, 4, 4, 4, 4, 4, 4, 3, 3],
            20: [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        }
    },
    "Sorcerer": {
        "HIT_DIE": "d4",
        "ALIGNMENT": ["Any"],
        "SKILL_POINTS": 2,
        "CLASS_SKILLS": [
            "Bluff", "Concentration", "Craft", "Knowledge (arcana)", "Profession", "Spellcraft"
        ],
        "WEAPONS": [
            "club", "dagger", "heavy crossbow", "light crossbow", "quarterstaff"
        ],
        "ARMOR": [],
        "SHIELDS": [],
        "SPECIAL_ABILITIES": {
            1: ["Summon Familiar"],
        },
        "BASE": [
            [0], [1], [1], [2], [2], [3], [3], [4], [4], [5],
            [5], [6], [6], [7], [7], [8], [8], [9], [9], [10]
        ],
        "FORT_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "REF_SAVE": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
        "WILL_SAVE": [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12],
        "SPELLS_PER_DAY": {
            1: [5, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            2: [6, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            3: [6, 5, 0, 0, 0, 0, 0, 0, 0, 0],
            4: [6, 6, 3, 0, 0, 0, 0, 0, 0, 0],
            5: [6, 6, 4, 0, 0, 0, 0, 0, 0, 0],
            6: [6, 6, 5, 0, 0, 0, 0, 0, 0, 0],
            7: [6, 6, 6, 3, 0, 0, 0, 0, 0, 0],
            8: [6, 6, 6, 4, 0, 0, 0, 0, 0, 0],
            9: [6, 6, 6, 5, 0, 0, 0, 0, 0, 0],
            10: [6, 6, 6, 6, 3, 0, 0, 0, 0, 0],
            11: [6, 6, 6, 6, 4, 0, 0, 0, 0, 0],
            12: [6, 6, 6, 6, 5, 0, 0, 0, 0, 0],
            13: [6, 6, 6, 6, 6, 3, 0, 0, 0, 0],
            14: [6, 6, 6, 6, 6, 4, 0, 0, 0, 0],
            15: [6, 6, 6, 6, 6, 5, 0, 0, 0, 0],
            16: [6, 6, 6, 6, 6, 6, 3, 0, 0, 0],
            17: [6, 6, 6, 6, 6, 6, 4, 0, 0, 0],
            18: [6, 6, 6, 6, 6, 6, 5, 0, 0, 0],
            19: [6, 6, 6, 6, 6, 6, 6, 3, 0, 0],
            20: [6, 6, 6, 6, 6, 6, 6, 4, 0, 0],
        }
    }
}

# Info about races according to d20 SRD 3.5
RACE_INFO = {
    "Human": {
        "ABILITY_MODIFIERS": {},
        "SIZE": "Medium",
        "BASE_SPEED": 30,
        "VISION": [],
        "SKILL_BONUSES": {},
        "BONUS_FEAT": 1,
        "EXTRA_SKILL_POINTS": {
            "first_level": 4,
            "each_level": 1
        },
        "LANGUAGES": {
            "automatic": ["Common"],
            "bonus": ["Any (other than secret languages such as Druidic)"]
        },
        "FAVORED_CLASS": "Any",
        "SPECIAL": [
            "1 extra feat at 1st level",
            "4 extra skill points at 1st level and 1 extra skill point at each additional level"
        ]
    },
    "Dwarf": {
        "ABILITY_MODIFIERS": {"CON": +2, "CHA": -2},
        "SIZE": "Medium",
        "BASE_SPEED": 20,
        "VISION": ["Darkvision 60 ft."],
        "SKILL_BONUSES": {
            "Appraise (related to stone/metal)": 2,
            "Craft (related to stone/metal)": 2
        },
        "BONUS_FEAT": 0,
        "EXTRA_SKILL_POINTS": {},
        "LANGUAGES": {
            "automatic": ["Common", "Dwarven"],
            "bonus": ["Giant", "Gnome", "Goblin", "Orc", "Terran", "Undercommon"]
        },
        "FAVORED_CLASS": "Fighter",
        "SPECIAL": [
            "+2 saving throws against poison",
            "+2 saving throws against spells and spell-like effects",
            "+1 attack vs. orcs and goblinoids",
            "+4 dodge bonus to AC against giants",
            "Stability: +4 bonus on ability checks to resist being bull rushed or tripped",
            "Stonecunning: +2 bonus on Search checks to notice unusual stonework"
        ]
    },
    "Elf": {
        "ABILITY_MODIFIERS": {"DEX": +2, "CON": -2},
        "SIZE": "Medium",
        "BASE_SPEED": 30,
        "VISION": ["Low-Light Vision"],
        "SKILL_BONUSES": {
            "Listen": 2,
            "Search": 2,
            "Spot": 2
        },
        "BONUS_FEAT": 0,
        "EXTRA_SKILL_POINTS": {},
        "LANGUAGES": {
            "automatic": ["Common", "Elven"],
            "bonus": ["Draconic", "Gnoll", "Gnome", "Goblin", "Orc", "Sylvan", "Celestial"]
        },
        "FAVORED_CLASS": "Wizard",
        "SPECIAL": [
            "Immunity to magic sleep effects",
            "+2 saving throw against enchantment spells or effects",
            "Notice secret doors: automatic Search check when passing within 5 ft."
        ]
    },
    "Gnome": {
        "ABILITY_MODIFIERS": {"CON": +2, "STR": -2},
        "SIZE": "Small",
        "BASE_SPEED": 20,
        "VISION": ["Low-Light Vision"],
        "SKILL_BONUSES": {
            "Listen": 2,
            "Craft (alchemy)": 2
        },
        "BONUS_FEAT": 0,
        "EXTRA_SKILL_POINTS": {},
        "LANGUAGES": {
            "automatic": ["Common", "Gnome"],
            "bonus": ["Draconic", "Dwarven", "Elven", "Giant", "Goblin", "Orc"]
        },
        "FAVORED_CLASS": "Rogue",
        "SPECIAL": [
            "+2 saving throws against illusions",
            "+1 attack bonus against kobolds and goblinoids",
            "+4 dodge bonus to AC against giants",
            "Add +1 to Difficulty Class for all illusion spells cast",
            "Familiarity with gnome weapons (hooked hammer, etc.)",
            "Speak with burrowing mammals (as per speak with animals, 1/day)"
        ]
    },
    "Half-Elf": {
        "ABILITY_MODIFIERS": {},
        "SIZE": "Medium",
        "BASE_SPEED": 30,
        "VISION": ["Low-Light Vision"],
        "SKILL_BONUSES": {
            "Listen": 1,
            "Search": 1,
            "Spot": 1
        },
        "BONUS_FEAT": 0,
        "EXTRA_SKILL_POINTS": {},
        "LANGUAGES": {
            "automatic": ["Common", "Elven"],
            "bonus": ["Any (other than secret languages such as Druidic)"]
        },
        "FAVORED_CLASS": "Any",
        "SPECIAL": [
            "Immunity to magic sleep effects",
            "+2 saving throw against enchantment spells or effects",
            "Elven Blood: For all effects related to race, a half-elf is considered an elf",
            "+2 Diplomacy and Gather Information checks",
            "Multitalented: Favored class is any"
        ]
    },
    "Half-Orc": {
        "ABILITY_MODIFIERS": {"STR": +2, "INT": -2, "CHA": -2},
        "SIZE": "Medium",
        "BASE_SPEED": 30,
        "VISION": ["Darkvision 60 ft."],
        "SKILL_BONUSES": {},
        "BONUS_FEAT": 0,
        "EXTRA_SKILL_POINTS": {},
        "LANGUAGES": {
            "automatic": ["Common", "Orc"],
            "bonus": ["Draconic", "Giant", "Gnoll", "Goblin", "Abyssal"]
        },
        "FAVORED_CLASS": "Barbarian",
        "SPECIAL": [
            "Orc Blood: For all effects related to race, a half-orc is considered an orc"
        ]
    },
    "Halfling": {
        "ABILITY_MODIFIERS": {"DEX": +2, "STR": -2},
        "SIZE": "Small",
        "BASE_SPEED": 20,
        "VISION": [],
        "SKILL_BONUSES": {
            "Climb": 2,
            "Jump": 2,
            "Move Silently": 2
        },
        "BONUS_FEAT": 0,
        "EXTRA_SKILL_POINTS": {},
        "LANGUAGES": {
            "automatic": ["Common", "Halfling"],
            "bonus": ["Dwarven", "Elven", "Gnome", "Goblin", "Orc"]
        },
        "FAVORED_CLASS": "Rogue",
        "SPECIAL": [
            "+2 saving throws against fear",
            "+1 attack bonus with thrown weapons and slings",
            "+4 dodge bonus to AC against giants"
        ]
    }
}

ITEMS = {
    "Weapons": [
        # Format: { "name": ..., "type": ..., "category": ..., "damage": ..., "critical": ..., "range": ..., "weight": ..., "properties": [...], "gold": ... }
        {"name": "club", "type": "simple", "category": "melee", "damage": "1d6", "critical": "x2", "range": None, "weight": 3, "properties": ["wooden"], "gold": 0},
        {"name": "dagger", "type": "simple", "category": "melee", "damage": "1d4", "critical": "19-20/x2", "range": 10, "weight": 1, "properties": ["thrown", "piercing", "slashing"], "gold": 2},
        {"name": "mace (light)", "type": "simple", "category": "melee", "damage": "1d6", "critical": "x2", "range": None, "weight": 4, "properties": ["bludgeoning"], "gold": 5},
        {"name": "mace (heavy)", "type": "simple", "category": "melee", "damage": "1d8", "critical": "x2", "range": None, "weight": 8, "properties": ["bludgeoning"], "gold": 12},
        {"name": "morningstar", "type": "simple", "category": "melee", "damage": "1d8", "critical": "x2", "range": None, "weight": 6, "properties": ["bludgeoning", "piercing"], "gold": 8},
        {"name": "quarterstaff", "type": "simple", "category": "melee", "damage": "1d6/1d6", "critical": "x2", "range": None, "weight": 4, "properties": ["double", "bludgeoning"], "gold": 0},
        {"name": "shortspear", "type": "simple", "category": "melee", "damage": "1d6", "critical": "x2", "range": 20, "weight": 3, "properties": ["thrown", "piercing"], "gold": 1},
        {"name": "sickle", "type": "simple", "category": "melee", "damage": "1d6", "critical": "x2", "range": None, "weight": 2, "properties": ["slashing"], "gold": 6},
        {"name": "spear", "type": "simple", "category": "melee", "damage": "1d8", "critical": "x3", "range": 20, "weight": 6, "properties": ["thrown", "piercing"], "gold": 2},
        {"name": "crossbow (light)", "type": "simple", "category": "ranged", "damage": "1d8", "critical": "19-20/x2", "range": 80, "weight": 4, "properties": ["reload", "piercing"], "gold": 35},
        {"name": "crossbow (heavy)", "type": "simple", "category": "ranged", "damage": "1d10", "critical": "19-20/x2", "range": 120, "weight": 8, "properties": ["reload", "piercing"], "gold": 50},
        {"name": "dart", "type": "simple", "category": "ranged", "damage": "1d4", "critical": "x2", "range": 20, "weight": 0.5, "properties": ["thrown", "piercing"], "gold": 0.5},
        {"name": "javelin", "type": "simple", "category": "ranged", "damage": "1d6", "critical": "x2", "range": 30, "weight": 2, "properties": ["thrown", "piercing"], "gold": 1},
        {"name": "sling", "type": "simple", "category": "ranged", "damage": "1d4", "critical": "x2", "range": 50, "weight": 0, "properties": ["bludgeoning"], "gold": 0},
        # Martial Melee
        {"name": "battleaxe", "type": "martial", "category": "melee", "damage": "1d8", "critical": "x3", "range": None, "weight": 6, "properties": ["slashing"], "gold": 10},
        {"name": "flail", "type": "martial", "category": "melee", "damage": "1d8", "critical": "x2", "range": None, "weight": 5, "properties": ["bludgeoning"], "gold": 8},
        {"name": "glaive", "type": "martial", "category": "melee", "damage": "1d10", "critical": "x3", "range": None, "weight": 10, "properties": ["slashing", "reach"], "gold": 8},
        {"name": "greataxe", "type": "martial", "category": "melee", "damage": "1d12", "critical": "x3", "range": None, "weight": 12, "properties": ["slashing"], "gold": 20},
        {"name": "greatclub", "type": "martial", "category": "melee", "damage": "1d10", "critical": "x2", "range": None, "weight": 8, "properties": ["bludgeoning"], "gold": 5},
        {"name": "greatsword", "type": "martial", "category": "melee", "damage": "2d6", "critical": "19-20/x2", "range": None, "weight": 8, "properties": ["slashing"], "gold": 50},
        {"name": "guisarme", "type": "martial", "category": "melee", "damage": "2d4", "critical": "x3", "range": None, "weight": 12, "properties": ["slashing", "reach", "trip"], "gold": 9},
        {"name": "halberd", "type": "martial", "category": "melee", "damage": "1d10", "critical": "x3", "range": None, "weight": 12, "properties": ["slashing", "piercing"], "gold": 10},
        {"name": "longsword", "type": "martial", "category": "melee", "damage": "1d8", "critical": "19-20/x2", "range": None, "weight": 4, "properties": ["slashing"], "gold": 15},
        {"name": "pick (heavy)", "type": "martial", "category": "melee", "damage": "1d6", "critical": "x4", "range": None, "weight": 6, "properties": ["piercing"], "gold": 8},
        {"name": "pick (light)", "type": "martial", "category": "melee", "damage": "1d4", "critical": "x4", "range": None, "weight": 3, "properties": ["piercing"], "gold": 4},
        {"name": "ranseur", "type": "martial", "category": "melee", "damage": "2d4", "critical": "x3", "range": None, "weight": 12, "properties": ["piercing", "reach"], "gold": 10},
        {"name": "rapier", "type": "martial", "category": "melee", "damage": "1d6", "critical": "18-20/x2", "range": None, "weight": 2, "properties": ["piercing"], "gold": 20},
        {"name": "scimitar", "type": "martial", "category": "melee", "damage": "1d6", "critical": "18-20/x2", "range": None, "weight": 4, "properties": ["slashing"], "gold": 15},
        {"name": "scythe", "type": "martial", "category": "melee", "damage": "2d4", "critical": "x4", "range": None, "weight": 10, "properties": ["slashing", "piercing"], "gold": 18},
        {"name": "shortsword", "type": "martial", "category": "melee", "damage": "1d6", "critical": "19-20/x2", "range": None, "weight": 2, "properties": ["piercing"], "gold": 10},
        {"name": "trident", "type": "martial", "category": "melee", "damage": "1d8", "critical": "x2", "range": 10, "weight": 4, "properties": ["thrown", "piercing"], "gold": 15},
        {"name": "warhammer", "type": "martial", "category": "melee", "damage": "1d8", "critical": "x3", "range": None, "weight": 5, "properties": ["bludgeoning"], "gold": 12},
        {"name": "whip", "type": "martial", "category": "melee", "damage": "1d3", "critical": "x2", "range": None, "weight": 2, "properties": ["slashing", "reach", "nonlethal"], "gold": 1},
        # Martial Ranged
        {"name": "longbow", "type": "martial", "category": "ranged", "damage": "1d8", "critical": "x3", "range": 100, "weight": 3, "properties": ["piercing"], "gold": 75},
        {"name": "longbow (composite)", "type": "martial", "category": "ranged", "damage": "1d8", "critical": "x3", "range": 110, "weight": 3, "properties": ["piercing"], "gold": 100},
        {"name": "shortbow", "type": "martial", "category": "ranged", "damage": "1d6", "critical": "x3", "range": 60, "weight": 2, "properties": ["piercing"], "gold": 30},
        {"name": "shortbow (composite)", "type": "martial", "category": "ranged", "damage": "1d6", "critical": "x3", "range": 70, "weight": 2, "properties": ["piercing"], "gold": 75},
        {"name": "throwing axe", "type": "martial", "category": "ranged", "damage": "1d6", "critical": "x2", "range": 10, "weight": 2, "properties": ["thrown", "slashing"], "gold": 8},
        # Exotic Melee
        {"name": "bastard sword", "type": "exotic", "category": "melee", "damage": "1d10", "critical": "19-20/x2", "range": None, "weight": 6, "properties": ["slashing"], "gold": 35},
        {"name": "spiked chain", "type": "exotic", "category": "melee", "damage": "2d4", "critical": "x2", "range": None, "weight": 10, "properties": ["piercing", "reach", "trip"], "gold": 25},
        {"name": "dire flail", "type": "exotic", "category": "melee", "damage": "1d8/1d8", "critical": "x2", "range": None, "weight": 10, "properties": ["double", "bludgeoning"], "gold": 90},
        {"name": "kama", "type": "exotic", "category": "melee", "damage": "1d6", "critical": "x2", "range": None, "weight": 2, "properties": ["slashing"], "gold": 2},
        {"name": "nunchaku", "type": "exotic", "category": "melee", "damage": "1d6", "critical": "x2", "range": None, "weight": 2, "properties": ["bludgeoning"], "gold": 2},
        {"name": "siangham", "type": "exotic", "category": "melee", "damage": "1d6", "critical": "x2", "range": None, "weight": 1, "properties": ["piercing"], "gold": 3},
        {"name": "sai", "type": "exotic", "category": "melee", "damage": "1d4", "critical": "x2", "range": 10, "weight": 1, "properties": ["bludgeoning"], "gold": 1},
        # Exotic Ranged
        {"name": "hand crossbow", "type": "exotic", "category": "ranged", "damage": "1d4", "critical": "19-20/x2", "range": 30, "weight": 2, "properties": ["reload", "piercing"], "gold": 100},
        {"name": "shuriken", "type": "exotic", "category": "ranged", "damage": "1d2", "critical": "x2", "range": 10, "weight": 0.1, "properties": ["thrown", "piercing"], "gold": 1},
        {"name": "bolas", "type": "exotic", "category": "ranged", "damage": "1d4", "critical": "x2", "range": 10, "weight": 2, "properties": ["thrown", "nonlethal"], "gold": 5},
        {"name": "net", "type": "exotic", "category": "ranged", "damage": None, "critical": None, "range": 10, "weight": 6, "properties": ["entangle"], "gold": 20}
    ],
    "Armor": [
        # Format: { "name": ..., "type": ..., "AC": ..., "max_dex": ..., "check_penalty": ..., "arcane_failure": ..., "speed_30": ..., "speed_20": ..., "weight": ..., "gold": ... }
        {"name": "padded", "type": "light", "AC": 1, "max_dex": 8, "check_penalty": 0, "arcane_failure": 5, "speed_30": 30, "speed_20": 20, "weight": 10, "gold": 5},
        {"name": "leather", "type": "light", "AC": 2, "max_dex": 6, "check_penalty": 0, "arcane_failure": 10, "speed_30": 30, "speed_20": 20, "weight": 15, "gold": 10},
        {"name": "studded leather", "type": "light", "AC": 3, "max_dex": 5, "check_penalty": -1, "arcane_failure": 15, "speed_30": 30, "speed_20": 20, "weight": 20, "gold": 25},
        {"name": "chain shirt", "type": "light", "AC": 4, "max_dex": 4, "check_penalty": -2, "arcane_failure": 20, "speed_30": 30, "speed_20": 20, "weight": 25, "gold": 100},
        {"name": "hide", "type": "medium", "AC": 4, "max_dex": 4, "check_penalty": -3, "arcane_failure": 20, "speed_30": 20, "speed_20": 15, "weight": 25, "gold": 15},
        {"name": "scale mail", "type": "medium", "AC": 4, "max_dex": 3, "check_penalty": -4, "arcane_failure": 25, "speed_30": 20, "speed_20": 15, "weight": 30, "gold": 50},
        {"name": "chainmail", "type": "medium", "AC": 5, "max_dex": 2, "check_penalty": -5, "arcane_failure": 30, "speed_30": 20, "speed_20": 15, "weight": 40, "gold": 150},
        {"name": "breastplate", "type": "medium", "AC": 5, "max_dex": 3, "check_penalty": -4, "arcane_failure": 25, "speed_30": 20, "speed_20": 15, "weight": 30, "gold": 200},
        {"name": "splint mail", "type": "heavy", "AC": 6, "max_dex": 0, "check_penalty": -7, "arcane_failure": 40, "speed_30": 20, "speed_20": 15, "weight": 45, "gold": 200},
        {"name": "banded mail", "type": "heavy", "AC": 6, "max_dex": 1, "check_penalty": -6, "arcane_failure": 35, "speed_30": 20, "speed_20": 15, "weight": 35, "gold": 250},
        {"name": "half-plate", "type": "heavy", "AC": 7, "max_dex": 0, "check_penalty": -7, "arcane_failure": 40, "speed_30": 20, "speed_20": 15, "weight": 50, "gold": 600},
        {"name": "full plate", "type": "heavy", "AC": 8, "max_dex": 1, "check_penalty": -6, "arcane_failure": 35, "speed_30": 20, "speed_20": 15, "weight": 50, "gold": 1500}
    ],
    "Shields": [
        # Format: { "name": ..., "AC": ..., "check_penalty": ..., "arcane_failure": ..., "weight": ..., "gold": ... }
        {"name": "buckler", "AC": 1, "check_penalty": -1, "arcane_failure": 5, "weight": 5, "gold": 15},
        {"name": "shield (light)", "AC": 1, "check_penalty": -1, "arcane_failure": 5, "weight": 6, "gold": 9},
        {"name": "shield (heavy)", "AC": 2, "check_penalty": -2, "arcane_failure": 15, "weight": 15, "gold": 20},
        {"name": "shield (tower)", "AC": 4, "check_penalty": -10, "arcane_failure": 50, "weight": 45, "gold": 30}
    ],
    "Helmets": [
        # Format: { "name": ..., "AC": ..., "weight": ..., "gold": ... }
        {"name": "helmet (common)", "AC": 1, "weight": 3, "gold": 10}
    ],
    "Gloves": [
        # Format: { "name": ..., "AC": ..., "weight": ..., "gold": ... }
        {"name": "gloves (common)", "AC": 0, "weight": 0.5, "gold": 5}
    ],
    "Boots": [
        # Format: { "name": ..., "AC": ..., "weight": ..., "gold": ... }
        {"name": "boots (common)", "AC": 0, "weight": 2, "gold": 5}
    ],
    "Rings": [
        # Format: { "name": ..., "AC": ..., "weight": ..., "gold": ... }
        {"name": "ring (common)", "AC": 0, "weight": 0, "gold": 50}
    ],
    "Necklace": [
        # Format: { "name": ..., "AC": ..., "weight": ..., "gold": ... }
        {"name": "necklace (common)", "AC": 0, "weight": 0.1, "gold": 100}
    ],
}

ITEM_MODIFIERS = [
    {
        "name": "masterwork",
        "applies_to": ["weapon", "armor", "shield"],
        "attack_bonus": 1,          # weapons only
        "armor_check_penalty": -1,  # armor/shields only
        "required_for_magic": True,
        "weight_multiplier": 1.0,
        "cost": 300                 # weapons: +300 gp, armor/shield: +150 gp
    },
    {
        "name": "silvered",
        "applies_to": ["weapon"],
        "damage_modifier": -1,
        "bypasses": ["damage reduction (silver)"],
        "weight_multiplier": 1.0,
        "cost": 20                  # +20 gp per ammo, +90 gp for light weapon, +180 gp for one/two-handed
    },
    {
        "name": "cold iron",
        "applies_to": ["weapon"],
        "damage_modifier": 0,
        "bypasses": ["damage reduction (cold iron)"],
        "weight_multiplier": 1.0,
        "cost_multiplier": 2.0      # double normal cost
    },
    {
        "name": "adamantine",
        "applies_to": ["weapon", "armor"],
        "damage_modifier": 0,
        "bypasses": ["hardness < 20", "damage reduction (adamantine)"],
        "armor_damage_reduction": {
            "light": 1,
            "medium": 2,
            "heavy": 3
        },
        "weight_multiplier": 1.0,
        "cost": {
            "weapon": 3000,
            "light_armor": 5000,
            "medium_armor": 10000,
            "heavy_armor": 15000
        }
    },
    {
        "name": "mithral",
        "applies_to": ["armor", "shield"],
        "weight_multiplier": 0.5,
        "max_dex_bonus": 2,         # increases max Dex bonus by 2
        "armor_check_penalty": 3,   # reduces penalty by 3
        "arcane_failure": 10,       # reduces arcane spell failure by 10%
        "cost": {
            "light_armor": 1000,
            "medium_armor": 4000,
            "heavy_armor": 9000,
            "shield": 1500
        }
    },
    {
        "name": "darkwood",
        "applies_to": ["shield", "weapon"],
        "weight_multiplier": 0.5,
        "armor_check_penalty": 2,   # reduces penalty by 2
        "cost": 10                  # +10 gp per pound
    }
]

GEAR = [
    {"name": "backpack", "weight": 2, "cost_gp": 2, "description": "Carries up to 2 cubic feet/40 lbs. of gear."},
    {"name": "bedroll", "weight": 5, "cost_gp": 0.1, "description": "Blanket for sleeping outdoors."},
    {"name": "bell", "weight": 0, "cost_gp": 1, "description": "Small metal bell."},
    {"name": "blanket, winter", "weight": 3, "cost_gp": 0.5, "description": "Keeps you warm in cold weather."},
    {"name": "block and tackle", "weight": 5, "cost_gp": 5, "description": "Pulley system for lifting up to 400 lbs."},
    {"name": "candle", "weight": 0, "cost_gp": 0.01, "description": "Burns for 1 hour, provides dim light."},
    {"name": "case, map or scroll", "weight": 0.5, "cost_gp": 1, "description": "Holds 10 rolled sheets of paper or parchment."},
    {"name": "chalk, 1 piece", "weight": 0, "cost_gp": 0.01, "description": "For marking surfaces."},
    {"name": "chest", "weight": 25, "cost_gp": 2, "description": "Holds up to 12 cubic feet/300 lbs. of gear."},
    {"name": "crowbar", "weight": 5, "cost_gp": 2, "description": "Grants +2 bonus on STR checks to force open doors."},
    {"name": "flask", "weight": 1.5, "cost_gp": 0.03, "description": "Holds 1 pint of liquid."},
    {"name": "grappling hook", "weight": 4, "cost_gp": 1, "description": "Thrown up to 20 ft., used for climbing."},
    {"name": "hammer", "weight": 2, "cost_gp": 0.5, "description": "Small hammer for driving pitons."},
    {"name": "ink (1 oz. vial)", "weight": 0, "cost_gp": 8, "description": "Black ink for writing."},
    {"name": "inkpen", "weight": 0, "cost_gp": 0.1, "description": "For writing with ink."},
    {"name": "jug, clay", "weight": 9, "cost_gp": 0.03, "description": "Holds 1 gallon of liquid."},
    {"name": "lamp, common", "weight": 1, "cost_gp": 0.1, "description": "Burns 6 hours on 1 pint of oil, 15-ft. radius light."},
    {"name": "lantern, bullseye", "weight": 3, "cost_gp": 12, "description": "60-ft. cone of bright light, burns 6 hours per pint of oil."},
    {"name": "lantern, hooded", "weight": 2, "cost_gp": 7, "description": "30-ft. radius bright light, burns 6 hours per pint of oil."},
    {"name": "lock (very simple)", "weight": 1, "cost_gp": 20, "description": "DC 20 Open Lock check."},
    {"name": "lock (average)", "weight": 1, "cost_gp": 40, "description": "DC 25 Open Lock check."},
    {"name": "lock (good)", "weight": 1, "cost_gp": 80, "description": "DC 30 Open Lock check."},
    {"name": "lock (amazing)", "weight": 1, "cost_gp": 150, "description": "DC 40 Open Lock check."},
    {"name": "manacles", "weight": 2, "cost_gp": 15, "description": "DC 30 Escape Artist or STR check to escape."},
    {"name": "mirror, small steel", "weight": 0.5, "cost_gp": 10, "description": "Useful for looking around corners."},
    {"name": "oil (1-pint flask)", "weight": 1, "cost_gp": 0.1, "description": "Burns 6 hours in lamp, can be thrown (1d3 fire damage)."},
    {"name": "paper (sheet)", "weight": 0, "cost_gp": 0.2, "description": "Sheet of paper for writing."},
    {"name": "parchment (sheet)", "weight": 0, "cost_gp": 0.1, "description": "Sheet of parchment for writing."},
    {"name": "piton", "weight": 0.5, "cost_gp": 0.1, "description": "Iron spike for climbing."},
    {"name": "pole, 10-foot", "weight": 8, "cost_gp": 0.2, "description": "Wooden pole, 10 feet long."},
    {"name": "pot, iron", "weight": 10, "cost_gp": 0.5, "description": "For cooking."},
    {"name": "pouch, belt", "weight": 0.5, "cost_gp": 1, "description": "Holds up to 1/5 cubic foot or 6 lbs. of gear."},
    {"name": "rations, trail (per day)", "weight": 1, "cost_gp": 0.5, "description": "Dry food for one day."},
    {"name": "rope, hempen (50 ft.)", "weight": 10, "cost_gp": 1, "description": "DC 15 to burst, 2 HP."},
    {"name": "rope, silk (50 ft.)", "weight": 5, "cost_gp": 10, "description": "DC 24 to burst, 4 HP."},
    {"name": "sack", "weight": 0.5, "cost_gp": 0.1, "description": "Holds up to 1 cubic foot/30 lbs. of gear."},
    {"name": "sealing wax", "weight": 0, "cost_gp": 1, "description": "For sealing letters."},
    {"name": "signal whistle", "weight": 0, "cost_gp": 0.8, "description": "Audible up to 1 mile."},
    {"name": "signet ring", "weight": 0, "cost_gp": 5, "description": "Personal seal for documents."},
    {"name": "soap (per lb.)", "weight": 1, "cost_gp": 0.5, "description": "For cleaning."},
    {"name": "spade or shovel", "weight": 8, "cost_gp": 2, "description": "For digging."},
    {"name": "spyglass", "weight": 1, "cost_gp": 1000, "description": "Magnifies distant objects x2."},
    {"name": "tent", "weight": 20, "cost_gp": 10, "description": "Shelters two people."},
    {"name": "torch", "weight": 1, "cost_gp": 0.01, "description": "Burns 1 hour, 20-ft. radius light."},
    {"name": "vial", "weight": 0, "cost_gp": 1, "description": "Holds 1 ounce of liquid."},
    {"name": "waterskin", "weight": 4, "cost_gp": 1, "description": "Holds 1/2 gallon of liquid."},
    {"name": "whetstone", "weight": 1, "cost_gp": 0.02, "description": "Sharpens blades."}
]

# All SKILLS as described in the D20 SRD 3.5
SKILLS = [
    {
        "name": "Appraise",
        "key_ability": "INT",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Estimate value of items."
    },
    {
        "name": "Balance",
        "key_ability": "DEX",
        "untrained": True,
        "armor_check_penalty": True,
        "description": "Keep your balance on narrow or slippery surfaces."
    },
    {
        "name": "Bluff",
        "key_ability": "CHA",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Convince others of falsehoods."
    },
    {
        "name": "Climb",
        "key_ability": "STR",
        "untrained": True,
        "armor_check_penalty": True,
        "description": "Scale walls and slopes."
    },
    {
        "name": "Concentration",
        "key_ability": "CON",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Maintain focus to cast spells or use abilities."
    },
    {
        "name": "Craft",
        "key_ability": "INT",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Create items (specify type: alchemy, armor, etc.)."
    },
    {
        "name": "Decipher Script",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Decode written messages."
    },
    {
        "name": "Diplomacy",
        "key_ability": "CHA",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Negotiate and influence attitudes."
    },
    {
        "name": "Disable Device",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Disarm traps, open locks, sabotage."
    },
    {
        "name": "Disguise",
        "key_ability": "CHA",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Alter appearance."
    },
    {
        "name": "Escape Artist",
        "key_ability": "DEX",
        "untrained": True,
        "armor_check_penalty": True,
        "description": "Slip out of bonds or grapples."
    },
    {
        "name": "Forgery",
        "key_ability": "INT",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Create or detect forgeries."
    },
    {
        "name": "Gather Information",
        "key_ability": "CHA",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Collect rumors and news."
    },
    {
        "name": "Handle Animal",
        "key_ability": "CHA",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Train and control animals."
    },
    {
        "name": "Heal",
        "key_ability": "WIS",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Treat wounds and diseases."
    },
    {
        "name": "Hide",
        "key_ability": "DEX",
        "untrained": True,
        "armor_check_penalty": True,
        "description": "Conceal yourself."
    },
    {
        "name": "Intimidate",
        "key_ability": "CHA",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Frighten or bully others."
    },
    {
        "name": "Jump",
        "key_ability": "STR",
        "untrained": True,
        "armor_check_penalty": True,
        "description": "Leap over obstacles."
    },
    {
        "name": "Knowledge (arcana)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Arcane magic and creatures."
    },
    {
        "name": "Knowledge (architecture and engineering)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Buildings, bridges, fortifications."
    },
    {
        "name": "Knowledge (dungeoneering)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Underground environments."
    },
    {
        "name": "Knowledge (geography)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Lands, terrain, climate."
    },
    {
        "name": "Knowledge (history)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Historical events, legends."
    },
    {
        "name": "Knowledge (local)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Local people, legends, laws."
    },
    {
        "name": "Knowledge (nature)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Animals, plants, seasons."
    },
    {
        "name": "Knowledge (nobility and royalty)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Nobles, heraldry, royalty."
    },
    {
        "name": "Knowledge (religion)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Deities, myths, religious traditions."
    },
    {
        "name": "Knowledge (the planes)",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Other planes of existence."
    },
    {
        "name": "Listen",
        "key_ability": "WIS",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Hear noises and conversations."
    },
    {
        "name": "Move Silently",
        "key_ability": "DEX",
        "untrained": True,
        "armor_check_penalty": True,
        "description": "Sneak without being heard."
    },
    {
        "name": "Open Lock",
        "key_ability": "DEX",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Pick locks."
    },
    {
        "name": "Perform",
        "key_ability": "CHA",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Entertain with music, acting, etc."
    },
    {
        "name": "Profession",
        "key_ability": "WIS",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Earn a living in a trade."
    },
    {
        "name": "Ride",
        "key_ability": "DEX",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Guide a mount."
    },
    {
        "name": "Search",
        "key_ability": "INT",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Find hidden objects or details."
    },
    {
        "name": "Sense Motive",
        "key_ability": "WIS",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Discern lies or intentions."
    },
    {
        "name": "Sleight of Hand",
        "key_ability": "DEX",
        "untrained": False,
        "armor_check_penalty": True,
        "description": "Pick pockets, palm objects."
    },
    {
        "name": "Spellcraft",
        "key_ability": "INT",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Identify spells and magic effects."
    },
    {
        "name": "Spot",
        "key_ability": "WIS",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Notice fine details or hidden creatures."
    },
    {
        "name": "Survival",
        "key_ability": "WIS",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Survive in the wild, track creatures."
    },
    {
        "name": "Swim",
        "key_ability": "STR",
        "untrained": True,
        "armor_check_penalty": True,
        "description": "Swim or keep afloat."
    },
    {
        "name": "Tumble",
        "key_ability": "DEX",
        "untrained": False,
        "armor_check_penalty": True,
        "description": "Dodge past opponents, avoid attacks."
    },
    {
        "name": "Use Magic Device",
        "key_ability": "CHA",
        "untrained": False,
        "armor_check_penalty": False,
        "description": "Activate magic items without normal requirements."
    },
    {
        "name": "Use Rope",
        "key_ability": "DEX",
        "untrained": True,
        "armor_check_penalty": False,
        "description": "Tie or untie knots, secure ropes."
    }
]
