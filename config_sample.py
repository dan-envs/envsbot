# ================= CONFIG =================
import logging

# === Logging ===
LOG_LEVEL = logging.INFO                    # Logging verbosity

# === Account data ===
JID = "<botname>@domain.tld/bot"            # JID of the bot
PASSWORD = "<password>"                     # Password of the bot
NICK = "<botname>"                          # Nick of the bot

# === Adminstration ===
ADMINS = ["<admim>@domain.tld"]             # Bot Administrators
# Rooms to join
ROOMS = ["<room>@conference.envs.net", ...]

# === Startup status ===
START_SHOW = "online"                       # online|chat|away|xa|dnd
START_STATUS = "I'm ready to serve you!"    # Startup status message
START_PRIORITY = 0                          # Startup priority

# === sqlite database ===
DB_FILE = "bot.db"                          # Bot sqlite DB

# === Avatar Data ===
AVATAR = "bot.jpg"                          # Avatar image file
AVATAR_TYPE = "image/jpeg"                  # Avatar image type

# === VCard ===
VCARD_XML = """
<vCard xmlns='vcard-temp'>
    <FN>Name of the bot, a service bot</FN>
    <NICKNAME>bluebot</NICKNAME>
    <BDAY>2026-03-08</BDAY>
    <ADR>
        <STREET/>
        <LOCALITY/>
        <REGION/>
        <PCODE/>
        <CTRY/>
    </ADR>
    <EMAIL>
        <AUTHOR/>
        <PREF/>
        <USERID><admin>@domain.tld</USERID>
    </EMAIL>
    <EMAIL>
        <OTHER/>
        <USERID><other>@domain.tld</USERID>
    </EMAIL>
    <JABBERID><botname>@domain.tld</JABBERID>
    <ORG>
        <ORGNAME>Organisation</ORGNAME>
        <ORGUNIT>XMPP server</ORGUNIT>
    </ORG>
    <TITLE>Automatic helper bot</TITLE>
    <URL>https://sub.domain.tld/</URL>
    <URL>https://github.com/<handle>/botname</URL>
    <TZ>Europe/Berlin</TZ>
    <NOTE>
I'm a bot which will have a lot of tools which will be all documented
inside the bot. I'm still in development, but my development
progresses. I'm still in an early stage of development and a lot
of functionality has still to be implemented.

You can send a XMPP subscription request to the above JABBERID/XNPP
address and I'll send a subscription request back, and if you accept
it, I'll automatically be added to your roster.
    </NOTE>
</vCard>
"""
