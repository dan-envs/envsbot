# ========== ENVS Bot ==========
import asyncio
import logging
import hashlib

from pathlib import Path

from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream import ET

import config

# === set up logging ===
logging.basicConfig(level=config.LOG_LEVEL)
log = logging.getLogger(__name__)


# ===== VCard into Dict ====
class VCardWrapper:
    VCARD_NS = "vcard-temp"

    def __init__(self, vcard_stanza):
        self.vcard = vcard_stanza

    def _findall(self, tag):
        # Alle Elemente eines Typs unter Berücksichtigung des Namespaces
        return self.vcard.xml.findall(f".//{{{self.VCARD_NS}}}{tag}")

    def _normalize_element(self, el):
        # Konvertiert ein Element in ein lesbares Dict oder Text
        if len(el):
            # Verschachtelte Elemente
            return {child.tag.split('}')[1]: child.text for child in el}
        return el.text

    def __getitem__(self, key):
        elements = self._findall(key)
        if not elements:
            return []
        # Immer eine Liste zurückgeben, für einfache Iteration
        return [self._normalize_element(el) for el in elements]

    def __setitem__(self, key, value):
        # Alte Elemente entfernen
        for el in self._findall(key):
            self.vcard.xml.remove(el)

        from xml.etree.ElementTree import Element

        def make_element(k, v):
            el = Element(f"{{{self.VCARD_NS}}}{k}")
            if isinstance(v, dict):
                for subkey, subval in v.items():
                    sub_el = Element(f"{{{self.VCARD_NS}}}{subkey}")
                    sub_el.text = subval
                    el.append(sub_el)
            else:
                el.text = v
            return el

        # Wert(e) hinzufügen
        if isinstance(value, list):
            for item in value:
                self.vcard.xml.append(make_element(key, item))
        else:
            self.vcard.xml.append(make_element(key, value))

    def __iter__(self):
        # Iterator über alle Top-Level-Elemente der vCard
        for el in self.vcard.xml:
            yield self._normalize_element(el)

    def __repr__(self):
        fields = [f"{el.tag.split('}')[1]}: {el.text}" for el in self.vcard.xml]
        return f"<VCardWrapper {', '.join(fields)}>"


# ===== Actual EnvsBot Class =====
class EnvsBot(ClientXMPP):
    """ A XMPP bot with various functions """

    def __init__(self, jid, password):
        """ Initialize bot and set event handlers

            Handlers:
                session_start(event)        - bot start event
                on_message(msg)             - got chat message
        """
        super().__init__(jid, password)

        # Register plugins
        self.register_plugin('xep_0030')    # Service Discovery
        self.register_plugin('xep_0045')    # Multi User Chat
        self.register_plugin('xep_0054')    # VCard
        self.register_plugin('xep_0163')    # PubSub / PEP (Basis)
        self.register_plugin('xep_0084')    # User Avatar

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.on_message)


    # ===== Callback for startup =====
    async def session_start(self, event):
        """ Called when session starts
            - Sets initial presence/status
            - get Roster
            - Joins rooms
        """
        self.status = {}
        self.status['show'] = config.START_SHOW
        self.status['status'] = config.START_STATUS
        self.status['priority'] = config.START_PRIORITY
        self.send_presence(pshow=self.status['show'],
                           pstatus=self.status['status'],
                           ppriority=self.status['priority'])
        await self.get_roster()

        for room in config.ROOMS:
            self.plugin["xep_0045"].join_muc(room, config.NICK,
                                             pstatus=self.status['status'],
                                             pshow=self.status['show'])

        # set automatic mutual subscriptions
        self.roster.auto_subscribe = True

        # VCard Setup
        await self.vcard_setup()

        # Bot started
        log.info("✅ Bot started, all rooms joined")

    # ===== PEP VCard and Avatar Initialization =====
    async def vcard_setup(self):
        # === VCARD Setup ===
        try:
            # -------------------------
            # 1. vCard via XEP-0054
            # -------------------------
            vcard = ET.fromstring(config.VCARD_XML)

            # IQ-Set senden
            await self['xep_0054'].publish_vcard(vcard)
            log.info("✅ vCard published with XEP-0054")

            # -------------------------
            # 2. Avatar via PEP/XEP-0084
            # -------------------------
            sha1_hash = hashlib.sha1(avatar).hexdigest()
            size = len(avatar)
            mime_type = config.AVATAR_TYPE
            # Avatar Data
            await self['xep_0084'].publish_avatar(avatar)
            # Avatar Metadata
            metadata = {
                    'id': sha1_hash,
                    'type': mime_type,
                    'bytes': str(size),
                    'replace': True
            }
            await self['xep_0084'].publish_avatar_metadata(metadata)
            log.info("✅ Avatar veröffentlicht via PEP")

        except (IqError, IqTimeout) as e:
            log.error(f"❌Couldn' publish Avatar and VCard: {e}")
        return

    # ===== Callback if message arrives =====
    async def on_message(self, msg):
        """ Callback, that's called when the bot gets a message """

        # ignore own messages
        if msg['type'] == "groupchat" and msg['mucnick'] == config.NICK:
            return

        # check if cmd
        if not msg['body'].startswith(','):
            return

        log.info(f"✅ Got Command: {msg}")
        # Check if msg is from admin
        if self.is_admin(msg['from'].bare):
            await self.admin_cmds(msg)
        else:
            await self.user_cmds(msg)

    # ===== helper functions =====
    # ===== Checks if a JID is bot admin =====
    def is_admin(self, jabberid):
        """ Checks if jid is bot admin """

        if jabberid in config.ADMINS:
            return True
        return False

    # ===== Send ephemeral message, which won't be stored on the server =====
    def send_ephemeral(self, mto: str, mtype: str, mbody):
        """
        Sends ephemeral message which doesn't get stored on the
        server.
        """

        msg = self.Message()
        msg['to'] = mto
        msg['type'] = mtype
        msg['body'] = mbody
        no_store = ET.Element("{urn:xmpp:hints}no-store")
        msg.append(no_store)
        msg.send()

    # ===== Show online/chat/away/xa/dnd status with comment =====
    def show_status(self, msg):
        """ Shows status to requesting JID """

        # show status
        if self.status['show'] == "online":
            send_body = f"✅ Online: {self.status['status']}"
        elif self.status['show'] == "chat":
            send_body = f"🗨 Free for chat: {self.status['status']}"
        elif self.status['show'] == "away":
            send_body = f"🫧 Away: {self.status['status']}"
        elif self.status['show'] == "xa":
            send_body = f"💤 Extended away: {self.status['status']}"
        elif self.status['show'] == "dnd":
            send_body = f"⛔Do not disturb: {self.status['status']}"
        else:
            send_body = "❌offline"
        mfrom = msg['from'] if msg['type'] == "chat" else msg['from'].bare
        self.send_message(mfrom, mtype=msg['type'], mbody=send_body)

    # ===== Set MUC status of bot =====
    def set_muc_status(self, room=None):
        """ Sends a presence to a room """

        if room is None:
            return
        pres = self.make_presence(pto=f"{room}/{config.NICK}")
        pres['show'] = self.status['show']
        pres['status'] = self.status['status']
        pres['priority'] = self.status['priority']
        pres.send()

    # ===== COMMANDS SECTION =====
    # ===== All Administrator Commands =====
    async def admin_cmds(self, msg):
        """ All administrator commands """

        parts = msg['body'].split()
        if len(parts) > 0:
            match parts[0]:
                case ",help" | ",h":
                    self.cmd_help(msg)
                case ",status" | ",s":
                    self.cmd_status(msg)
                case ",roster" | ",r":
                    self.cmd_roster(msg)
                case ",vcard" | ",v":
                    await self.cmd_vcard(msg)
                case _:
                    return

    # ===== All User Commands =====
    async def user_cmds(self, msg):
        """ All user commands """

        parts = msg['body'].split()
        if len(parts) > 0:
            match parts[0]:
                case ",help" | ",h":
                    self.cmd_help(msg)
                case ",status" | ",s":
                    self.cmd_status(msg)
                case ",vcard" | ",v":
                    await self.cmd_vcard(msg)
                case _:
                    return

    # ===== Help Command (,help) =====
    def cmd_help(self, msg):
        """ Shows different help files for users and admins """

        nick = msg['mucnick'] if msg['mucnick'] is not None else ""
        if self.is_admin(msg['from'].bare):
            send_body = (f"{nick + " - " if nick != "" else ""}==ADMIN=="
                         + f"Help:\n{ADMIN_HELP}")
        else:
            send_body = f"{nick + " - " if nick != "" else ""}==USER== Help:"
            if msg['type'] == "groupchat":
                send_body += " Help only in direct chat. No spamming!"
            else:
                send_body += f"\n{USER_HELP}"
        mfrom = msg['from'] if msg['type'] == "chat" else msg['from'].bare
        self.send_message(mfrom, mtype=msg['type'], mbody=send_body)

    # ===== Status command (,status) =====
    def cmd_status(self, msg):
        """
        Show/Set presence for bot and participated rooms

        Admin:
          - <,s|,status> [chat|online|away|xa|dnd [status comment]]
            shows status if rest is omitted or garbled. Otherwise sets status.
        User:
          - <,s|,status>
            shows status
        """

        parts = msg['body'].split()
        if (self.is_admin(msg['from'].bare) and len(parts) >= 2
                and parts[1] in ["chat", "online", "away", "xa", "dnd"]):
            # build and send bot presence
            self.status['show'] = parts[1]
            if len(parts) >= 3:
                self.status['status'] = " ".join(parts[2:])
            else:
                self.status['status'] = ""
            self.status['priority'] = 0
            self.send_presence(pshow=self.status['show'],
                               pstatus=self.status['status'],
                               ppriority=self.status['priority'])
            # set presence of bot in all rooms
            for room in config.ROOMS:
                self.set_muc_status(room=room)
            # show status
            self.show_status(msg)
        else:
            # just show status
            self.show_status(msg)

    # ===== Roster Command (,roster) =====
    def cmd_roster(self, msg):
        """ Outputs Bot's roster """

        # Check, if user is admin
        if not self.is_admin(msg['from'].bare):
            self.send_message(msg['from'], mtype=msg['type'],
                              mbody="❌Restricted command")
            return
        output = f"=={config.NICK}== Roster:\n"
        for x in self.roster.keys():
            for key in self.roster[x]:
                output += f"{key}: Subscription: "
                output += f"{self.roster[x][key]['subscription']}\n"
            break
        self.send_message(msg['from'], mtype=msg['type'], mbody=output)
        return

    # ===== VCard Command (,vcard) =====
    async def cmd_vcard(self, msg):
        """ Gets own or other users VCard """

        parts = msg['body'].split()
        if len(parts) < 2:
            jabberid = msg['from']
        elif len(parts) == 2:
            jabberid = parts[1]
            if msg['type'] == "groupchat" and "@" not in parts[1]:
                jabberid = msg['from'].bare + "/" + parts[1]
        else:
            self.send_message(msg['from'], mtype=msg['type'],
                              mbody="❌Command malformed")
            return
        log.info(f"✅ Requested VCard for: {jabberid}")
        try:
            output = f"=={jabberid}== VCard:\n"
            # get VCard
            vcard = await asyncio.wait_for(
                self['xep_0054'].get_vcard(jabberid), timeout=5)

            # prepare output
            tree = VCardWrapper(vcard)
            if tree["FN"]:
                output += f"Full Name: {tree["FN"]}\n"
            if tree["NICKNAME"]:
                output += f"Nickname: {tree["NICKNAME"]}\n"
            if tree["BDAY"]:
                output += f"Birthday: {tree["BDAY"]}\n\n"
            for email in tree["EMAIL"] if tree['EMAIL'] else None:
                output += "Email"
                for key in email:
                    if key != "USERID":
                        output += f" ({key})\n"
                output += f": <{email['USERID']}>\n"
            if tree["JABBERID"]:
                output += f"JabberID: {tree["JABBERID"]}\n"
            for url in tree["URL"] if tree["URL"] else None:
                output += f"URL: {url}\n"
            if tree["TZ"]:
                output += f"Timezone: {tree["TZ"]}\n\n"
            if tree["ORG"]:
                if tree["ORG"]["ORGNAME"]:
                    output += f"Organisation: {tree["ORG"]["ORGNAME"]}\n"
                if tree["ORG"]["ORGUNIT"]:
                    output += f"Org. Unit: {tree["ORG"]["ORGUNIT"]}\n"
            if tree["TITLE"]:
                output += f"Title: {tree["TITLE"]}\n\n"
            for note in tree["NOTE"] if tree["Note"] else None:
                output += f"Note: ---\n{note}\n"

            # send output back
            mfrom = msg['from'] if msg['type'] == "chat" else msg['from'].bare
            self.send_message(mfrom, mtype=msg['type'], mbody=output)
        except Exception as e:
            mfrom = msg['from'] if msg['type'] == "chat" else msg['from'].bare
            self.send_message(mfrom, mtype=msg['type'],
                              mbody="❌No vcard-temp found for "
                              + f"'{jabberid}': {e}")
        return


# ===== MAIN ROUTINE =====
if __name__ == '__main__':
    # === Get Help Files to display ===
    ADMIN_HELP = Path('admin_help.txt').read_text()
    USER_HELP = Path('user_help.txt').read_text()

    # === Load bot avatar ===
    with open(config.AVATAR, mode="rb") as image:
        avatar = image.read()
    # avatar_b64 = base64.b64encode(avatar).decode('utf-8')

    # === Start Bot ===
    xmpp = EnvsBot(config.JID, config.PASSWORD)
    if xmpp.connect():
        log.info("Connected successfully. Starting event loop...")
        try:
            # Run the slixmpp event loop forever
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            # Gracefully shut down on CTRL-c
            log.info("Bot stopped manually.")
            xmpp.disconnect()
    else:
        log.error("Unable to connect to XMPP server.")
