import discord
from discord.ext import commands

import jishaku
import os
import sys

from core.database import SQL # pylint: disable=import-error

class Admin(commands.Cog):
    def __init__(self, bot):
        """Комманды для владельца бота."""
        self.bot = bot
        self.sql = SQL(bot.db).sql

    async def cog_check(self, ctx):
        if await self.bot.is_owner(ctx.author):
            return True
        else:
            raise commands.NotOwner()

    @commands.command(hidden=True, aliases=['reboot'])
    async def restart(self, ctx):
        await ctx.send('> Restart')
        os.execl(sys.executable, sys.executable, *sys.argv) # nosec

    @commands.group(name="sql", 
        invoke_without_command=True, 
        hidden=True)
    async def sql_cmd(self, ctx, *, code: jishaku.codeblocks.codeblock_converter):
        """Исполнить запрос к PostgreSQL."""
        requests = code.content.split(";")
        out = []
        line = 0
        returned = "RESULT\n\n"

        for request in requests:
            if not request:  # '' case
                continue

            try:
                answer = await self.sql(request)

            except Exception as e:
                answer = f"{type(e).__name__}:  {e}"

            out.append(answer)

        for result in out:
            returned += f"Line {line}: ```{result}```\n\n"
            line += 1

        if len(returned) > 1997:
            returned = returned[:1997] + "..."

        await ctx.send(returned)

    @sql_cmd.command(hidden=True)
    async def backup(self, ctx):
        """Создать резервную копию базы данных."""
        os.system(f'pg_dump {self.bot.config["sqlPath"]} > backup.psql') # nosec

        await ctx.author.send(
            "Backup loaded",
            file=discord.File("backup.psql"))

    @commands.command(hidden=True)
    async def update(self, ctx):
        """Git pull and restart of the bot"""
        if os.system('git pull') != 0:
            return await ctx.send('Error')
        await ctx.invoke(self.restart)

def setup(bot):
    cog = Admin(bot)
    bot.add_cog(cog)

