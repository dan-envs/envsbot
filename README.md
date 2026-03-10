# BlueBot XMPP Tool Bot

XMPP Bot with some tools for day to day life in an XMPP chat room.

## Supported so far

* **,help**: Displays help for user/admin
* **,status**: Show bot status (presence)
* **,status set &lt;show&gt; \[comment\]**: Set bot status (admin command)
* **,plugins <list|load|reload|unload> \[args\]**: Manage Plugins

## TODO
- [ ] ',roster' command
- [X] Setting avatar and vcard in separate module (reg_profile.py)
- [ ] General database support sqlite3 for admins, rooms, etc.
