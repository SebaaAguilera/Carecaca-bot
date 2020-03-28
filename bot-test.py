# bot.py

# System
import os
import asyncio


# Discord
import discord
import logging
from dotenv import load_dotenv
from discord.ext import commands


# Custom
import Models.Card
import Models.Player
import GameController.GameController as gc
import Display.TextDisplay as td

load_dotenv()
TEST_TOKEN = os.getenv('DISCORD_TEST_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

Keviinplz = int(os.getenv('KEVIN_ID'))
Sebakun = int(os.getenv('SEBA_ID'))



client = discord.Client()
bot = commands.Bot(command_prefix='!')

bot.load_extension("cogs.General")
bot.load_extension("cogs.GameControls")
bot.load_extension("cogs.InGameControls")
bot.load_extension("cogs.AdminCommands")


# =============================================================================================
# ====================================== Log Status ===========================================
# =============================================================================================

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord-log.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# =============================================================================================
# ====================================== Class ================================================
# =============================================================================================

##gameController = gc.GameController()
bot.gcDict = {}
bot.ADMIN_LIST = [Keviinplz, Sebakun]
# Keviinplz ID


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, Bienvenido al Servidor Oficial de CareCaca!'
    )


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord! \n')
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


bot.run(TEST_TOKEN)
