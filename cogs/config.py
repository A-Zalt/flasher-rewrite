
import discord
from discord.ext import commands
from core.database import LocaleSQL, PrefixesSQL

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.localeSQL = LocaleSQL(bot.db, bot.config)
        self.prefixesSQL = PrefixesSQL(bot.db, bot.config)

    async def set_locale(self, ctx, obj, language):
        """Sets language."""
        if language not in self.bot.locales.keys():
            languages = ', '.join([f'`{lang}`' for lang in self.bot.locales.keys()])
            
            embed = discord.Embed(title=ctx['config.locale.notexists'],
                description=ctx._('config.locale.notexists.description', languages=languages),
                color=discord.Colour.dark_red())
            
            await ctx.send(embed=embed)
            return
        
        await self.localeSQL.set(obj, language)
        embed = discord.Embed(title=ctx['config.locale.succesfull'],
            color=discord.Colour.dark_green())
        await ctx.send(embed=embed)

    async def set_prefix(self, ctx, obj, value):
        if len(value) > 7:
            return await ctx.send(ctx['prefix.toolong'])

        if value in ctx['prefix.reset']:
            await self.prefixesSQL.reset(obj)
            embed = discord.Embed(color=discord.Colour.dark_blue(),
                title=ctx['prefix.reset.succesfull'])
            return await ctx.send(embed=embed)

        await self.prefixesSQL.set(obj, value)

        embed=discord.Embed(color=discord.Colour.green(),
            title=ctx['prefix.succesfull'])
        await ctx.send(embed=embed)

    @commands.group(aliases=['locatization', 'language' ,'lang'],
        invoke_without_command=True)
    async def locale(self, ctx):
        user_current = await self.localeSQL.get(ctx.author)
        guild_current = await self.localeSQL.get(ctx.guild) if ctx.guild else ctx['config.locale.get.notAGuild']

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

    @commands.group(invoke_without_command=True)
    async def prefix(self, ctx):
        user_prefix = await self.prefixesSQL.get(ctx.author) or ctx['config.prefix.notset']
        guild_prefix = await self.prefixesSQL.get(ctx.guild) or ctx['config.prefix.notset'] if ctx.guild else ctx['config.prefix.notguild']
        
        embed = discord.Embed(description=ctx._('config.prefix.status', 
            user_prefix, guild_prefix, self.bot.config['prefix']))
        
        await ctx.send(embed=embed)

    @prefix.command(name='user', aliases=['self'])
    async def prefix_user(self, ctx, value: str):
        await self.set_prefix(ctx, ctx.author, value)


    @prefix.command(name='server', aliases=['guild'])
    @commands.guild_only()
    async def prefix_server(self, ctx, value: str):
        await self.set_prefix(ctx, ctx.guild, value)

def setup(bot):
    bot.add_cog(Configuration(bot))