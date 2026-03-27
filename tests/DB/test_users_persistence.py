import json
import aiosqlite
import pytest

from database.users import UserManager


@pytest.mark.asyncio
async def test_runtime_persisted_to_db_after_flush():
    """
    Integration-style test: use the real UserManager + PluginRuntimeStore,
    set runtime data and call flush_all(). Verify the users_runtime row
    is written and contains the expected JSON and timestamp.
    """
    conn = await aiosqlite.connect(":memory:")
    conn.row_factory = aiosqlite.Row

    try:
        um = UserManager(conn)
        await um.init()

        jid = "persist@example"
        # create user (marks dirty_users so flush_all will insert the users row)
        await um.create(jid, nickname="p")

        store = um.plugin("myp")

        # set a runtime value for the plugin (cached only until flush)
        await store.set(jid, "alpha", {"x": 1})

        # sanity checks before flush
        assert jid in um._runtime_cache
        assert jid in um._dirty_runtime
        assert jid in um._dirty_users
        assert jid in um._runtime_meta
        ts_before = um._runtime_meta[jid]

        # perform the flush which should write both users and runtime rows
        await um.flush_all()

        # after flush, dirty sets should be cleared
        assert not um._dirty_runtime
        assert not um._dirty_users

        # verify persisted runtime row
        cursor = await conn.execute(
            "SELECT data, last_updated FROM users_runtime WHERE jid = ?",
            (jid,),
        )
        row = await cursor.fetchone()
        assert row is not None, "Expected a users_runtime row after flush_all()"

        data_text, last_updated = row
        data = json.loads(data_text)

        # verify plugin data persisted
        assert "plugins" in data
        assert "myp" in data["plugins"]
        assert data["plugins"]["myp"]["alpha"] == {"x": 1}

        # verify last_updated matches the runtime_meta timestamp that was
        # flushed
        assert last_updated == ts_before

    finally:
        await conn.close()
