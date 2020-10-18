from discord.ext import commands
import traceback
import logging
from time import ctime

from .files import load as load_config
from .extensions import load as load_extensions

class BotClass(commands.AutoShardedBot):
    """The main class of a bot."""
    def __init__(self):
        self.config = load_config()
        super().__init__(self.config['prefix'], 
            help_command=None) # Disables standart help command

        self._extensions_loaded = False

    async def on_ready(self):
        if not self._extensions_loaded: # Loading extensions if not previously loaded
            load_extensions(self)
            self._extensions_loaded = True

        logging.info(f'Ready at {ctime()}. Logged in as {self.user.name} (ID:{self.user.id})')