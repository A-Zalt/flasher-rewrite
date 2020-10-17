#!/usr/bin/python3
import discord
from discord.ext import commands

import core.bot
import core.files

if __name__ == "__main__":
    config = core.files.load()
    core.files.change_environment_variables()
    
    bot = core.bot.BotClass()
    bot.run(config['token'])