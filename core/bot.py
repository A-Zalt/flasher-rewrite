from discord.ext import commands
import logging
import traceback
from time import ctime

from .config import load as load_config

logging.basicConfig(level=logging.INFO,
            format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
            handlers=[
                logging.FileHandler(f"logs/{ctime()}.log"),
                logging.StreamHandler()
            ])

class BotClass(commands.AutoShardedBot):
    """The main class of a bot."""
    def __init__(self):
        self.config = load_config()
        super().__init__(self.config['prefix'])

        self._extensions_loaded = False

    async def on_ready(self):
        if not self._extensions_loaded: # Loading extensions if not previously loaded
            load_extensions(self)
            self._extensions_loaded = True

        logging.info(f'Ready at {ctime()}. Logged in as {self.user.name} (ID:{self.user.id})')

def load_extensions(bot: commands.Bot or commands.AutoShardedBot, extensions: tuple=None):
    """Loads bot extensions.

    Arguments
    ---------
    bot: commands.Bot or commands.AutoShardedBot - Bot class
    extensions: tuple = None - Custom extensions list. If not provided function will get it from the config by yourself"""
    if not extensions:
        extensions = load_config()['extensions']
    
    for extension in extensions:
            try:
                bot.load_extension(extension)
                logging.info(f"An extension \"{extension}\" loaded")
            except:
                error = traceback.format_exc()
                logging.error(f"An extension \"{extension}\" is not loaded.\n" + error)






