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
        guild_lang = self.bot.languages[self.guild.id] if self.guild and self.guild.id in self.bot.languages.keys() else None
        user_lang = self.bot.languages[self.author.id] if self.author.id in self.bot.languages.keys() else None
        base_lang = self.bot.config['locale.base']

        if (lang := user_lang):
            pass
        elif (lang := guild_lang):
            pass
        else:
            lang = base_lang
        
        try:
            strings = self.bot.locales[lang]
        except KeyError: # In case of lang='not_a_language'
            strings = self.bot.locales[base_lang]

        value = strings.get(string,
            f'[{lang}:{string} translation required]')
        
        return value.format(*args, **kwargs)

    def __getitem__(self, string: str): # ctx['string']
        return self._(string)