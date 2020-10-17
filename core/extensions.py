import logging
import traceback
from .config import load as load_config

def load(bot: commands.Bot or commands.AutoShardedBot, extensions: tuple=None):
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
            except: #pylint: disable=bare-except
                error = traceback.format_exc()
                logging.error(f"An extension \"{extension}\" is not loaded.\n" + error)



