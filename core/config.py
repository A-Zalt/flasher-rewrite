from pathlib import Path
from logging import debug, info
import yaml
import os

def load(path: str='config.yaml'):
    """Loads the bot config.
    
    Arguments
    ---------
    
    path: str = 'config.yaml' - Path to config file"""
    file = Path(path).open()
    result = yaml.safe_load(file)

    debug('Config loaded and parsed succesful')

    return result

def change_environment_variables():
    """Reads from file environment.yaml values and changes environment variables."""
    values = load('environment.yaml')

    for key in values.keys():
        os.environ[key] = values[key]

    info(f'Changed environment variables to {values}')