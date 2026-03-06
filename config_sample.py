# ================= CONFIG =================
import logging

# === Logging ===
LOG_LEVEL = logging.INFO                    # Logging verbosity

# === Account data ===
JID = "edna@domain.tld"                     # JID of the bot
PASSWORD = "yourpassword"                   # Password of the bot
NICK = "edna"                               # Nick of the bot

# === Adminstration ===
ADMINS = ["admin@domain.tld"]               # Bot Administrators
ROOMS = ["<room>@muc.domain.tld"]           # Rooms the bot should join
# Startup status show <online|chat|away|xa|dnd>
START_SHOW = "online"
START_STATUS = "I'm ready to serve you!"    # Startup status message

# === sqlite database ===
DB_FILE = "bot.db"                          # Bot sqlite DB
