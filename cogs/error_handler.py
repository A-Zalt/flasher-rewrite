import traceback
import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        check = lambda errorToCheck: isinstance(error, errorToCheck)
        generate_embed = lambda description: discord.Embed(
            color=discord.Colour.dark_red(),
            title='Похоже была вызвана ошибка во время исполнения команды...',
            description=description)

        if check(commands.CommandNotFound):
            return

        elif check(commands.NotOwner):
            embed = generate_embed('Вы не являетесь владельцем бота что бы исполнить эту команду!')

        else:
            embed = None

        if embed:
            return await ctx.send(embed=embed)

        embed_public = discord.Embed(color=discord.Colour.dark_red(),
            title='Вызвана неизвестная ошибка',
            description='Разработчик бота уже уведомлён об этой ошибке.\n'
            'Нажмите на заголовок чтобы перейти на сервер поддержки.',
            url=self.bot.config['invite'])

        err = '\n'.join(
            traceback.format_exception(
                type(error), error, error.__traceback__))

        if len(err) > 1500:
            err = '...\n' + err[-512:]

        embed_private = discord.Embed(title='Unknown error catched',
            description=f'Guild ID: `{ctx.guild.id if ctx.guild else 0}`. \n Author ID: `{ctx.author.id}`\n'
            f'Channel ID: `{ctx.channel.id}` \n Content: `{ctx.message.content}`\n'
            f'```py\n{err}\n```')

        if await self.bot.is_owner(ctx.author):
            return await ctx.send(embed=embed_private)

        errors_channel = await self.bot.fetch_channel(self.bot.config['channels.errors'])

        await errors_channel.send(embed=embed_private)

        await ctx.send(embed=embed_public,
            delete_after=120)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
