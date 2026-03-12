"""
User database management.

This module implements persistent user handling for the bot.

It manages three database tables:

users
    Core identity information. Contains the JID and frequently updated fields.
users_profile
    Stores rarely changing profile information as JSON.
users_runtime
    Stores dynamic runtime/plugin data as JSON.

JSON fields support nested key/value access using dotted paths.

Features
--------
- automatic user creation
- nested JSON access
- runtime/profile caching
- lazy database writes
- plugin-safe runtime namespaces
"""

import json


class PluginRuntimeStore:
    """
    Namespaced runtime storage for a plugin.

    Ensures plugins only access their own namespace in users_runtime.
    """

    def __init__(self, user_manager, plugin_name):
        self.um = user_manager
        self.plugin = plugin_name

    async def get(self, jid, key=None):
        """Return a runtime value for this plugin."""
        base = f"plugins.{self.plugin}"

        if key:
            path = f"{base}.{key}"
        else:
            path = base

        runtime = await self.um.get_runtime(jid)
        return await self.um.get_value(runtime, path)

    async def set(self, jid, key, value):
        """Set a runtime value for this plugin."""
        path = f"plugins.{self.plugin}.{key}"
        await self.um.set_runtime_value(jid, path, value)

    async def increment(self, jid, key, amount=1):
        """Increment a numeric runtime value."""
        current = self.get(jid, key)

        if current is None:
            current = 0

        await self.set(jid, key, current + amount)

    async def delete(self, jid, key):
        """Delete a key from the plugin namespace."""
        data = await self.um.get_runtime(jid)

        keys = f"plugins.{self.plugin}.{key}".split(".")
        target = data

        for k in keys[:-1]:
            target = target.get(k, {})

        target.pop(keys[-1], None)

        await self.um._dirty_runtime.add(jid)


class UserManager:
    """
    Manages user records, profile data, and runtime data.

    Provides caching and lazy write-back to reduce database load.
    """

    def __init__(self, db):
        self.db = db

        self._runtime_cache = {}
        self._profile_cache = {}

        self._dirty_runtime = set()
        self._dirty_profile = set()

    # ------------------------------------------------------------------
    # Database initialization
    # ------------------------------------------------------------------

    async def init(self):
        """Create required database tables if they do not exist."""

        await self.db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            jid TEXT PRIMARY KEY,
            nickname TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP
        )
        """)

        await self.db.execute("""
        CREATE TABLE IF NOT EXISTS users_profile (
            jid TEXT PRIMARY KEY,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data TEXT NOT NULL,
            FOREIGN KEY (jid) REFERENCES users(jid)
        )
        """)

        await self.db.execute("""
        CREATE TABLE IF NOT EXISTS users_runtime (
            jid TEXT PRIMARY KEY,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data TEXT NOT NULL,
            FOREIGN KEY (jid) REFERENCES users(jid)
        )
        """)

    # ------------------------------------------------------------------
    # User handling
    # ------------------------------------------------------------------

    async def create(self, jid, nickname=None):
        """Create a user if it does not exist."""
        await self.db.execute(
            """
            INSERT OR IGNORE INTO users (jid, nickname)
            VALUES (?, ?)
            """,
            (jid, nickname)
        )

    async def get(self, jid):
        """Return a user row."""
        return await self.db.fetch_one(
            "SELECT * FROM users WHERE jid=?",
            (jid,)
        )

    async def get_role(self, jid: str):
        """
        Return the role of a user or None if the user does not exist.
        """

        query = """
        SELECT role
        FROM users
        WHERE jid = ?
        """

        async with self.db.execute(query, (jid,)) as cursor:
            row = await cursor.fetchone()

        if row:
            return row["role"]
        return None

    async def update_last_seen(self, jid):
        """Update the last_seen timestamp."""
        await self.db.execute(
            """
            UPDATE users
            SET last_seen=CURRENT_TIMESTAMP
            WHERE jid=?
            """,
            (jid,)
        )

    async def delete_user(self, jid):
        """
        Completely remove a user from all tables and caches.

        This deletes the user's identity, profile data, and runtime data
        from the database and clears any cached entries.
        """

        # remove from database tables
        await self.db.execute("DELETE FROM users_runtime WHERE jid=?", (jid,))
        await self.db.execute("DELETE FROM users_profile WHERE jid=?", (jid,))
        await self.db.execute("DELETE FROM users WHERE jid=?", (jid,))

        # remove from caches
        self._runtime_cache.pop(jid, None)
        self._profile_cache.pop(jid, None)

        # remove from dirty tracking
        self._dirty_runtime.discard(jid)
        self._dirty_profile.discard(jid)

    # ------------------------------------------------------------------
    # JSON loading helpers
    # ------------------------------------------------------------------

    async def _load_json(self, table, jid, cache):
        """Load JSON data from the database or cache."""
        if jid in cache:
            return cache[jid]

        row = await self.db.fetch_one(
            f"SELECT data FROM {table} WHERE jid=?",
            (jid,)
        )

        if row:
            data = json.loads(row["data"])
        else:
            data = {}

        cache[jid] = data
        return data

    async def _write_json(self, table, jid, data):
        """Write JSON data to the database."""
        json_data = json.dumps(data)

        await self.db.execute(
            f"""
            INSERT INTO {table} (jid, data, last_updated)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(jid)
            DO UPDATE SET
                data=excluded.data,
                last_updated=CURRENT_TIMESTAMP
            """,
            (jid, json_data)
        )

    # ------------------------------------------------------------------
    # Profile access
    # ------------------------------------------------------------------

    async def get_profile(self, jid):
        """Return the user's profile JSON."""
        return await self._load_json(
            "users_profile",
            jid,
            self._profile_cache
        )

    async def set_profile_value(self, jid, key_path, value):
        """Set a nested profile value."""
        await self.set_value(
            self._profile_cache,
            self._dirty_profile,
            jid,
            key_path,
            value
        )

    # ------------------------------------------------------------------
    # Runtime access
    # ------------------------------------------------------------------

    async def get_runtime(self, jid):
        """Return the user's runtime JSON."""
        return await self._load_json(
            "users_runtime",
            jid,
            self._runtime_cache
        )

    async def set_runtime_value(self, jid, key_path, value):
        """Set a nested runtime value."""
        await self.set_value(
            self._runtime_cache,
            self._dirty_runtime,
            jid,
            key_path,
            value
        )

    # ------------------------------------------------------------------
    # Nested JSON helpers
    # ------------------------------------------------------------------

    async def get_value(self, data, key_path):
        """Return a nested value using dotted key paths."""
        keys = key_path.split(".")
        value = data

        for k in keys:
            if not isinstance(value, dict):
                return None

            value = value.get(k)

            if value is None:
                return None

        return value

    async def set_value(self, cache, dirty_set, jid, key_path, value):
        """Set a nested value inside cached JSON."""
        data = cache.setdefault(jid, {})

        keys = key_path.split(".")
        target = data

        for k in keys[:-1]:
            target = target.setdefault(k, {})

        target[keys[-1]] = value

        dirty_set.add(jid)

    # ------------------------------------------------------------------
    # Cache flushing
    # ------------------------------------------------------------------

    async def flush_runtime(self):
        """Write dirty runtime data to the database."""
        for jid in self._dirty_runtime:
            data = self._runtime_cache[jid]
            await self._write_json("users_runtime", jid, data)

        self._dirty_runtime.clear()

    async def flush_profile(self):
        """Write dirty profile data to the database."""
        for jid in self._dirty_profile:
            data = self._profile_cache[jid]
            await self._write_json("users_profile", jid, data)

        self._dirty_profile.clear()

    async def flush_all(self):
        """Flush all cached data to the database."""
        await self.flush_runtime()
        await self.flush_profile()

    # ------------------------------------------------------------------
    # Plugin storage API
    # ------------------------------------------------------------------

    def plugin_store(self, plugin_name):
        """
        Return a namespaced runtime storage object for a plugin.
        """
        return PluginRuntimeStore(self, plugin_name)
