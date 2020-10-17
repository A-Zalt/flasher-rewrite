#!/usr/bin/python3
import discord
from discord.ext import commands

import core.bot
import core.config

if __name__ == "__main__":
    config = core.config.load()
    core.config.change_environment_variables()
    
    bot = core.bot.BotClass()
    bot.run(config['token'])