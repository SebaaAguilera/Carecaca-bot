# bot.py
import os

import discord
from discord import Role
import random
from dotenv import load_dotenv
from discord.ext import commands
import card
import player

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

# inGameVariables
INGAME = False
WANT_TO_RESTART = False
PLAYERS = []
deck = []
stackCards = []

# Game Functions


def deleteData():
    INGAME = False
    WANT_TO_RESTART = False
    PLAYERS = []
    deck = card.deck().sort()
    stackCards = []
    # delete category


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, Bienvenido al Servidor Oficial de CareCaca!'
    )

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

# Functions
async def create_new_role(guild: discord.Guild, role_name: str, **kargs) -> Role:
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if not existing_role:
        new_role = await guild.create_role(name=role_name, **kargs)
        print(f'Creating a new role: {role_name}')
        return new_role
    else:
        await existing_role.edit(**kargs)
        print(f'Role {role_name} already exists!')
        return existing_role

async def delete_role(ctx, role_name):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        print(f'Deleting role: {role.name}')
        await role.delete()

@bot.command(name="testing", help="testing command")
async def testing(ctx):
    guild = ctx.guild
    await create_new_role(guild, "testing", mentionable=True, colour=discord.Colour(0x09c48c))

@bot.command(name='start', help='Start a new game')
async def startGame(ctx):
    if INGAME:
        WANT_TO_RESTART = True
        await ctx.send("u sure?")
    else:
        await ctx.send("let's begin")


@bot.command(name='yes', help='Aproves the reStart')
async def yesRestart(ctx):
    if WANT_TO_RESTART:
        await ctx.send("restarting")


@bot.command(name='no', help='Disaproves the restart')
async def dontRestart(ctx):
    if WANT_TO_RESTART:
        WANT_TO_RESTART = False
        await ctx.send("ok")

@bot.command(name="createRole", help="Create a role with name <name>")
async def createRole(ctx, *args):
    guild = ctx.guild
    await guild.create_role(name="{}".format(args[0]), colour=discord.Colour(0x09c48c))
    beautifulMsg = discord.Embed(title='{} has been created'.format(args[0]))
    await ctx.send("New role created", embed=beautifulMsg)

@bot.command(name="addRole", help="Add an existing role to message author player")
async def addRole(ctx, *args):
    role = discord.utils.get(ctx.guild.roles, name="{}".format(args[0]))
    user = ctx.message.author
    await user.add_roles(role)
    beautifulMsg = discord.Embed(title='Role {} has been added to player {}'.format(args[0], user))
    await ctx.send("New role assigned", embed=beautifulMsg)

@bot.command(name="startGame", help="Parte el juego")
async def startGame(ctx):
    members = ctx.message.guild.members
    guild = ctx.guild
    for member in members:
        if member.name == "Carecaca-bot":
            continue
        role_name = "jugador" + member.name    
        await create_new_role(guild, role_name, mentionable=True, colour=discord.Colour(0x09c48c))
        
    for member in members:
        role_name = "jugador" + member.name   
        role = discord.utils.get(guild.roles, name=role_name)
        if role:        
            await member.add_roles(role)

@bot.command(name="endGame", help="Termina el juego")
async def endGame(ctx):
    guild = ctx.guild
    members = ctx.message.guild.members
    for member in members:
        role_name = "jugador" + member.name 
        await delete_role(ctx, role_name)



bot.run(TOKEN)
