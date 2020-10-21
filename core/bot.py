import discord
from discord.ext import commands

import logging
import asyncpg

from .files import load_locales
from .extensions import load as load_extensions
from .database import SQL, CREATE_TABLES, LocaleSQL, PrefixesSQL
from .context import CustomContext

class BotClass(commands.AutoShardedBot):
    """The main class of a bot."""
    def __init__(self, config: dict, db: asyncpg.pool.Pool):
        """Initiates a bot class.

        Arguments
        ---------
        config: dict - Bot config
        db: asyncpg.pool.Pool - Database pool"""
        super().__init__(self.get_prefix,
            help_command=None) # Disables standart help command
        self.config = config
        self.db = db

        self._extensions_loaded = False

        self._prefixesSQL = PrefixesSQL(db, config)
        self._localeSQL = LocaleSQL(db, config)
        self.locales = load_locales()

    async def on_ready(self):
        if not self._extensions_loaded: # Loading extensions if not previously loaded
            load_extensions(self)
            self._extensions_loaded = True

        logging.info(f'Ready. Logged in as {self.user.name} (ID:{self.user.id})')

    async def get_context(self, msg, *, cls=CustomContext):
        ctx = await super().get_context(msg, cls=cls)
        ctx.language = await self.get_language(msg)
        return ctx

    async def get_language(self, msg):
        guild_lang = await self._localeSQL.get(msg.guild) if msg.guild else None
        user_lang = await self._localeSQL.get(msg.guild)
        base_lang = self.config['locale.base']

        lang = user_lang or guild_lang or base_lang

        if not lang in self.locales.keys():
            lang = base_lang
        return lang
        
    async def get_prefix(self, msg):
        guild_prefix = await self._prefixesSQL.get(msg.guild) if msg.guild else None
        user_prefix = await self._prefixesSQL.get(msg.author)
        base_prefix = self.config['prefix']

        return commands.when_mentioned_or((user_prefix or guild_prefix or base_prefix))(self, msg)

    async def on_message_edit(self, _, msg):
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