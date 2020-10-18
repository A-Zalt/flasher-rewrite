#!/usr/bin/python3
import discord
from discord.ext import commands

import asyncio
from logging import info

import core.bot
import core.files
import core.logs


if __name__ == "__main__":
    core.logs.setup()

    config = core.files.load()
    core.files.change_environment_variables()
    
    loop = asyncio.get_event_loop()

    run = core.bot.run(config)

    try:
        loop.run_until_complete(run)
    except KeyboardInterrupt:
        info("KeyboardInterrupt")