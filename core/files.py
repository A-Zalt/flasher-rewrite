from pathlib import Path
from logging import debug, info
import yaml
import os

def load(path: str='config.yaml'):
    """Loads yaml file.
    
    Arguments
    ---------
    
    path: str = 'config.yaml' - Path to config file. By default bot config"""
    file = Path(path).open()
    result = yaml.safe_load(file)

    info(f'YAML file {path} loaded and parsed succesful')

    return result

def change_environment_variables():
    """Reads from file environment.yaml values and changes environment variables."""
    values = load('environment.yaml')

    for key in values.keys():
        os.environ[key] = values[key]

    info(f'Changed environment variables to {values}')