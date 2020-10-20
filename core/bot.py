from discord.ext import commands
import traceback
import logging
import asyncpg
from time import ctime

from .files import load as load_config
from .files import load_locales
from .extensions import load as load_extensions
from .database import SQL, CREATE_TABLES, LocaleSQL
from .context import CustomContext

class BotClass(commands.AutoShardedBot):
    """The main class of a bot."""
    def __init__(self, config: dict, db: asyncpg.pool.Pool):
        """Initiates a bot class.

        Arguments
        ---------
        config: dict - Bot config
        db: asyncpg.pool.Pool - Database pool"""
        super().__init__(config['prefix'],
            help_command=None) # Disables standart help command
        self.config = config
        self._extensions_loaded = False
        self._localeSQL = LocaleSQL(db, self.config)
        self.locales = load_locales()
        self.languages = {} # 407524032292847624: uk_UA

    async def on_ready(self):
        if not self._extensions_loaded: # Loading extensions if not previously loaded
            load_extensions(self)
            self._extensions_loaded = True

        logging.info(f'Ready at {ctime()}. Logged in as {self.user.name} (ID:{self.user.id})')

    async def get_context(self, message, *, cls=CustomContext):
        return await super().get_context(message, cls=cls)

    async def on_message(self, msg):
        self.languages[msg.author.id] = await self._localeSQL.get(msg.author) # 407524032292847624: uk_UA
        if msg.guild:
            self.languages[msg.guild] = await self._localeSQL.get(msg.guild)
        await self.process_commands(msg)

async def run(config: dict):
    """Coroutine which starts bot and connects database."""
    try:
        db = await asyncpg.create_pool(config["sqlPath"])
        logging.info("PostgreSQL database connected.")
    except: # pylint: disable=bare-except
        logging.error("Database not connected, stoping.")
        exit(1)

    sql = SQL(db).sql

    for request in CREATE_TABLES:
        await sql(request)

    bot = BotClass(config, db)

    await bot.start(config["token"], reconnect=True, bot=True)