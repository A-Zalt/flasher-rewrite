from pathlib import Path
from logging import debug
import yaml


def load(path: str='config.yaml'):
    """Loads the bot config.
    
    Arguments
    ---------
    
    path: str = 'config.yaml' - Path to config file"""
    file = Path(path).open()
    result = yaml.safe_load(file)

    debug('Config loaded and parsed succesful')

    return result