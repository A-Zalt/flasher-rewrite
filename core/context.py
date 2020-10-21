from discord.ext import commands

class CustomContext(commands.Context):
    """Custom context for bot"""
    def _(self, string: str, *args, **kwargs):
        """Getting localization strings.

        Arguments
        ---------
        string: str - Localization string name
        args, kwargs - Arguments for format()

        Returns
        ---------
        Localization string for ctx.author"""
        
        strings = self.bot.locales[self.language]
        value = strings.get(string,
            f'[{self.language}:{string} translation required]')
        
        return value.format(*args, **kwargs)

    def __getitem__(self, string: str): # ctx['string']
        return self._(string)