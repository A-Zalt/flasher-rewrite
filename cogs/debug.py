import discord
from discord.ext import commands

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def l10n(self, ctx):
        await ctx.send(ctx['debug.l10n'])

    @l10n.command()
    async def format(self, ctx):
        await ctx.send(ctx._('debug.l10n.format', botname=self.bot.user.name))

    @l10n.command()
    async def notexists(self, ctx):
        await ctx.send(ctx['debug.l10n.notexists'])

    @commands.command()
    async def argument_check(self, ctx, arg: int):
        await ctx.send(arg)

def setup(bot):
    bot.add_cog(Debug(bot))