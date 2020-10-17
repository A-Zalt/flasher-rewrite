import discord
from discord.ext import commands

import sys
sys.dont_write_bytecode = True

import core.bot
import core.config

if __name__ == "__main__":
    config = core.config.load()
    
    bot = core.bot.BotClass()
    bot.run(config['token'])