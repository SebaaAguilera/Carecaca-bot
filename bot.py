# bot.py

# System
import os
import asyncio


# Discord
import discord
import logging
from discord import Role
from discord.ext.commands import CheckFailure
from dotenv import load_dotenv
from discord.ext import commands


# Custom
import card
import player
import gameController as gc
import textDisplay as td

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

Keviinplz = int(os.getenv('KEVIN_ID'))
Sebakun = int(os.getenv('SEBA_ID'))

ADMIN_LIST = [Keviinplz, Sebakun]

client = discord.Client()
bot = commands.Bot(command_prefix='!')

bot.load_extension("cogs.general")
bot.load_extension("cogs.gamecontrols")
bot.load_extension("cogs.ingamecontrols")


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




# =============================================================================================
# ====================================== Functions ============================================
# =============================================================================================

def is_any_user(ids):
    def predicate(ctx):
        return ctx.message.author.id in ids
    return commands.check(predicate)

# =============================================================================================
# ====================================== Admin Commands =======================================
# =============================================================================================

    @bot.command(pass_context=True)
    @is_any_user(ADMIN_LIST)
    async def broadcast(ctx, *, msg):
        for servers in bot.guilds:
            for channel in servers.text_channels:
                await channel.send(f'{msg}')

    @broadcast.error
    async def toall_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':x: **Sorry bro, you are not aloud to do that**')

    @bot.command(name="clear", help="Clear text channel")
    @is_any_user(ADMIN_LIST)
    async def clear(ctx, amount=100):
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=amount):
            messages.append(message)
        await channel.delete_messages(messages)
        await ctx.send(f'{len(messages)} messages deleted by {ctx.message.author.name}.')

    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':x: **Sorry bro, you are not aloud to do that**')


bot.run(TOKEN)
