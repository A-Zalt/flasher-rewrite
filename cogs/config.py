
import discord
from discord.ext import commands
from core.database import LocaleSQL

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = LocaleSQL(bot.db, bot.config)

    async def set_locale(self, ctx, obj, language):
        """Sets language."""
        if language not in self.bot.locales.keys():
            languages = ', '.join([f'`{lang}`' for lang in self.bot.locales.keys()])
            
            embed = discord.Embed(title=ctx['config.locale.notexists'],
                description=ctx._('config.locale.notexists.description', languages=languages),
                color=discord.Colour.dark_red())
            
            await ctx.send(embed=embed)
            return
        
        await self.db.set(obj, language)
        embed = discord.Embed(title=ctx['config.locale.succesfull'],
            color=discord.Colour.dark_green())
        await ctx.send(embed=embed)

    @commands.group(aliases=['locatization', 'language' ,'lang'], 
        invoke_without_command=True)
    async def locale(self, ctx):
        user_current = await self.db.get(ctx.author)
        guild_current = await self.db.get(ctx.guild) if ctx.guild else ctx['config.locale.get.notAGuild']
            
        embed = discord.Embed(title=ctx['config.locale.get.title'], 
            description=ctx._('config.locale.get.description', 
                user=user_current, guild=guild_current),
            color=discord.Colour.gold())

        return await ctx.send(embed=embed)

    @locale.command(name='user', aliases=['self'])
    async def locale_user(self, ctx, language: str):
        await self.set_locale(ctx, ctx.author, language)        

    @locale.command(name='server', aliases=['guild'])
    @commands.guild_only()
    async def locale_server(self, ctx, language: str):
        await self.set_locale(ctx, ctx.guild, language)

def setup(bot):
    bot.add_cog(Configuration(bot))