import asyncio
import logging
import aiosqlite

from .users import UserManager
from .rooms import Rooms

# logger for this module
log = logging.getLogger(__name__)


class DatabaseManager:
    """
    Central database manager.

    Handles the SQLite connection and exposes
    table managers for users and rooms.

    Also runs a background task that periodically
    flushes cached user data to the database.
    """

    def __init__(self, path: str, flush_interval: int = 60):

        self.path = path
        self.conn = None

        self.users = None
        self.rooms = None

        self.flush_interval = flush_interval
        self._flush_task = None
        self._running = False

    async def connect(self):
        """Open the database connection and initialize tables."""

        self.conn = await aiosqlite.connect(self.path)
        self.conn.row_factory = aiosqlite.Row

        self.users = UserManager(self.conn)
        self.rooms = Rooms(self.conn)

        await self.users.init()
        await self.rooms.init()

        # add asyncio sqlite3 stop event
        self._stop_event = asyncio.Event()

        # start background flush task
        self._running = True
        self._flush_task = asyncio.create_task(self._flush_loop())

    async def _flush_loop(self):
        try:
            while not self._stop_event.is_set():
                try:
                    await asyncio.wait_for(
                        self._stop_event.wait(),
                        timeout=self.flush_interval
                    )
                except asyncio.TimeoutError:
                    pass
                if self.users:
                    await self.users.flush_all()
        finally:
            # final guaranteed flush
            if self.users:
                await self.users.flush_all()

    async def flush(self):
        """Manually flush cached data."""

        if self.users:
            await self.users.flush_all()

    async def close(self):
        """
        Stop background tasks, flush caches, and close the database.
        """

        # signal shutdown
        self._stop_event.set()

        if self._flush_task:
            await self._flush_task

        if self.conn:
            await self.conn.close()
