from pathlib import Path
from logging import debug, info, warn
import yaml
import os

def load(path: str='config.yaml'):
    """Loads yaml file.
    
    Arguments
    ---------
    
    path: str = 'config.yaml' - Path to config file. By default bot config"""
    file = Path(path).open()
    result = yaml.safe_load(file)

    debug(f'YAML file {path} loaded and parsed succesful')

    return result

def change_environment_variables():
    """Reads from file environment.yaml values and changes environment variables."""
    values = load('environment.yaml')

    for key in values.keys():
        os.environ[key] = values[key]

    info(f'Changed environment variables to {values}')

def load_locales(folder: str='locale'):
    """Loads .yaml localization files.

    Arguments
    ---------
    folder: str = 'locale' - Folder with localization files

    Returns
    ---------
    Dictionary with localizations. Example:
    ```
    {
    'ru_RU':{'language.name.full': 'Русский (Россия)'},
    'en_US':{'language.name.full': 'English (United States)'}
    }
    ```"""
    files = {}
    locales = {}
    for file in os.scandir(folder):
        files[file.path] = file.name.replace('.yaml','') # 'locale/en_US.yaml' : 'en_US'

    for path in files.keys():
        try:
            result = load(path)
            
            if not isinstance(result, dict):
                raise TypeError('The localization file is not created correctly (dictionary excepted)')

            locales[files[path]] = result # locales['en_US'] : {}
        except Exception as e:
            warn(f'Failed to load "{path}" locale. {type(e).__name__}: {str(e)}')
        else:
            info(f'Locale {path} succesfully loaded')

    return locales