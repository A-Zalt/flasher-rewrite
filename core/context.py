from discord.ext import commands

class CustomContext(commands.Context):
    """Custom context for bot"""
    def _(self, string: str, *args, **kwargs):
        """Getting localization strings.

        Arguments
        ---------
        string: str - Localization string name
        _lack - What to return in case of lack of localization
        args, kwargs - Arguments for format()

        Returns
        ---------
        Localization string for ctx.author"""

        strings = self.bot.locales[self.language]
        value = strings.get(string,
            kwargs.pop('_lack', f'[{self.language}:{string} translation required]'))
        
        return value.format(*args, **kwargs) if isinstance(value, str) else value # In case of _lack=False

    def __getitem__(self, string: str): # ctx['string']
        return self._(string)