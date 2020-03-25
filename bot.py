# bot.py

# System
import os
import asyncio
import time


# Discord
import discord
import logging
from discord import Role
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

# =============================================================================================
# ====================================== Log Status ===========================================
# =============================================================================================


client = discord.Client()
bot = commands.Bot(command_prefix='!')

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

gameController = gc.GameController()


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

# create_new_role
# guild: discord.Guild role_name: str **kargs: args
# Create a new role


async def create_new_role(guild: discord.Guild, role_name: str, **kargs) -> Role:
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if not existing_role:
        print(f'Creating a new role: {role_name}')
        new_role = await guild.create_role(name=role_name, **kargs)
        return new_role
    else:
        await existing_role.edit(**kargs)
        return None


async def create_role(ctx, member, guild: discord.Guild, role_name: str, **kargs):
    role = await create_new_role(guild, role_name, mentionable=True, colour=discord.Colour(0x09c48c))
    if role != None:
        print(f'Role {role.name} has been created successfuly')
        await add_role_to_player(ctx, role, member)
    else:
        print(f'Role {role_name} already exists!')

# add_role_to_player
# role_name:str member: discord.Guild.member obj
# Add role to Player


async def add_role_to_player(ctx, role, member):
    print(f'Adding role: {role.name} to {member.name}')
    await member.add_roles(role)
    print(f'Role {role.name} has been asigment to {member.name}')
    await asign_member_to_object_player(member)


# assign_member_to_object_player
# role: discord.Role obj
# Connect Player objecto to Member with Role Member.
async def asign_member_to_object_player(member):
    pl = player.Player(member.name)
    print(f'Object player {pl.getId()} has been assigned to {member.name}')
    gameController.setPlayer(pl)


# delete_role
# ctx:obj role_name:str
# Delete an existing role
async def delete_role(ctx, role_name):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        print(f'Deleting role: {role.name}')
        await role.delete()


# manage_text_channel
# ctx:obj channel_name:str status:str category:discord.Category
# Can create and remove channel (depends of status)
async def manage_text_channel(ctx, channel_name, status, category):
    guild = ctx.message.guild
    message = ctx.message
    if status == "add":
        # Remove Permissions for @everyone
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),
        }
        # Create channel without permission for @everyone
        print(f'Creating text channel: {channel_name}')
        await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
    elif status == "remove":
        channels = category.channels
        for channel in channels:
            # Searching channel
            if channel.name == channel_name:
                # Delete Channel
                print(f'Deleting channel: {channel.name}')
                await channel.delete()
    else:
        # Catch wrong use of 'status' attribute in function
        print(f'Wrong attribute: {status}')
        return 0

# set_premission_text_channel
# ctx:obj channel_name:str role_name:str category:discord.Category
# Set Permission from role to Text Channel


async def set_permission_text_channel(ctx, channel_name, role_name, category):
    guild = ctx.message.guild
    channels = category.channels
    # Get Role object
    role = discord.utils.get(guild.roles, name=role_name)
    for channel in channels:
        # Searching Channel
        if channel.name == channel_name:
            # Set Permission to role @role_name
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = True
            overwrite.read_messages = True
            overwrite.view_channel = True
            # Now @role_name can view channel, send and read messages
            await channel.set_permissions(role, overwrite=overwrite)

# =============================================================================================
# ====================================== Bot Commands =========================================
# =============================================================================================

# General Commands


@bot.command(name="clear", help="Clear text channel")
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount):
        messages.append(message)
    await channel.delete_messages(messages)
    await ctx.send(f'{len(messages)} messages deleted by {ctx.message.author.name}.')


@bot.command(name="start-game", help="Start a CareCaca game")
async def startGame(ctx, *args):
    if len(args) > 0:
        if args[0] == "True":
            gameController.setFlash(True)
        elif args[0] == "False":
            gameController.setFlash(False)
        else:
            e = discord.Embed(
                title=':x: Invalid argument, if you wanna play with Flash use ``!start-game True``', colour=discord.Colour(0xff3232))
            await ctx.send("", embed=e)
            return

    await ctx.send(f'{ctx.message.author.name} has started a Carecaca Game')
    await ctx.send("Preparing room...")
    members = ctx.message.guild.members
    guild = ctx.guild

    # Text Channels will agrupate in category 'Players'
    main_category = await guild.create_category_channel("Players")

    # Creating roles and assigm them to Player
    for i in range(len(members)):
        if members[i].name == "Carecaca-bot":
            continue
        if members[i].status != discord.Status.offline:
            role_name = "player-" + str(i)
            channel_name = role_name
            await create_role(ctx, members[i], guild, role_name, mentionable=True, colour=discord.Colour(0x09c48c))
            await manage_text_channel(ctx, channel_name, "add", main_category)
            await set_permission_text_channel(ctx, channel_name, role_name, main_category)

    e = discord.Embed(title=':white_check_mark: Room is ready, please join to your Text Channel',
                      colour=discord.Colour(0x09c48c))
    await ctx.send('', embed=e)

    gameController.initGame()

    display = td.TextDisplay(gameController).outPutTextDisplay()
    categories = guild.categories
    channels = []
    for category in categories:
        if category.name == "Players":
            channels = category.channels

    for i in range(len(display)):
        await channels[i].send(f'{display[i]}')


@bot.command(name="end-game", help="End a CareCaca game")
async def endGame(ctx):
    await ctx.send(f'{ctx.message.author.name} has ended the game')
    await ctx.send('Deleting room...')
    guild = ctx.guild
    members = ctx.message.guild.members
    category = discord.utils.get(guild.categories, name="Players")

    # Deleting Roles
    for i in range(len(members)):
        if members[i].name == "Carecaca-bot":
            continue
        if members[i].status != discord.Status.offline:
            role_name = "player-" + str(i)
            channel_name = role_name
            await delete_role(ctx, role_name)
            await manage_text_channel(ctx, channel_name, "remove", category)

    # Deleting category 'Players'
    await category.delete(reason="End game")

    await ctx.send('Room has been deleted')

    gameController.resetController()


@bot.command(name="emoji", help="testing emoji messages")
async def emoji(ctx):
    await ctx.send(':regional_indicator_a:')

    await ctx.send('Room was delete')


@bot.command(name="hi", help="Say Hi to CareCaca bot!")
async def hi(ctx):
    await ctx.send(f'Hi {ctx.message.author.name}, nice to meet you! :heart:')


@bot.command(name="get-players", help="Print currently players (???")
async def get_players(ctx):
    players = botHelper.getPlayers()
    string = ""
    for player in players:
        string += player.getId() + "\n"
    e = discord.Embed(title=f'{string}')
    await ctx.send(f"Jugadores conectados: \n", embed=e)

# =============================================================================================
# ====================================== Game Commands ========================================
# =============================================================================================

# No cacho bien como funcionan las funciones acá, 
# Pero se podria colocar esta funcion en todos los comandos a excepcion de takeAll, no estoy eguro de como se haría en takeAll
# Pero iria en el if the gc.playing, despues de instanciar al player, reemplazando todo lo demás
def sendMsgToCtr(ctx,functionCall):
    guild = ctx.guild
    display = td.TextDisplay(gameController)
    if (functionCall):  #### aqui llegaria el putBlablabla 
        categories = guild.categories
        channels = []
        message = display.outPutTextDisplay()
        for category in categories:
            if category.name == "Players":
                channels = category.channels
    ctx.send(
            ":x: UwU Algo pasa`")

        for i in range(len(message)):
            await channels[i].send(f'{message[i]}')


# !p <cardNumber>
#
@bot.command(name="p")
async def p(ctx, *, args):
    if gameController.playing:
        guild = ctx.guild
        player = gameController.getPlayerById(ctx.message.author.name)
        display = td.TextDisplay(gameController)
        """
        cardOnTop = gameController.getCardOnTop()
        turnOwner = gameController.getTurnOwner()
        gameController.putCardFromHand(player, valor(args)) 
        print(cardOnTop is not gameController.getCardOnTop())
        print(f'Dueño del Turno: {gameController.getTurnOwner().getId()}')
        print(f'Valor turnOwner: {turnOwner.getId()}')
        print(turnOwner is not gameController.getTurnOwner())
        if cardOnTop is not gameController.getCardOnTop() or turnOwner is not gameController.getTurnOwner(): """
        if (gameController.putCardFromHand(player, valor(args))):
            categories = guild.categories
            channels = []
            message = display.outPutTextDisplay()
            for category in categories:
                if category.name == "Players":
                    channels = category.channels
            """        
            print(channels)
            print("")
            print(message)"""
            for i in range(len(message)):
                await channels[i].send(f'{message[i]}')
        else:
            await ctx.send('Si estoy aquí, tu wea ta mala')

    else:
        ctx.send(
            ":x: Nobody is playing now. If you want to start a game, use ``!start-game``")


@bot.command(name="t")
async def t(ctx, *, args):
    if gameController.playing:
        guild = ctx.guild
        player = gameController.getPlayerById(ctx.message.author.name)
        display = td.TextDisplay(gameController)
        if (gameController.putCardFromVisible(player, valor(args))):
            categories = guild.categories
            channels = []
            message = display.outPutTextDisplay()
            for category in categories:
                if category.name == "Players":
                    channels = category.channels

            for i in range(len(message)):
                await channels[i].send(f'{message[i]}')

    else:
        ctx.send(
            ":x: Nobody is playing now. If you want to start a game, use ``!start-game``")


@bot.command(name="h")
async def h(ctx, *, args):
    if gameController.playing:
        guild = ctx.guild
        player = gameController.getPlayerById(ctx.message.author.name)
        display = td.TextDisplay(gameController)
        if (gameController.putCardFromHidden(player, valor(args))):
            categories = guild.categories
            channels = []
            message = display.outPutTextDisplay()
            for category in categories:
                if category.name == "Players":
                    channels = category.channels

            for i in range(len(message)):
                await channels[i].send(f'{message[i]}')

    else:
        ctx.send(
            ":x: Nobody is playing now. If you want to start a game, use ``!start-game``")

# list
@bot.command(name="n")
async def n(ctx):
    if gameController.playing:
        guild = ctx.guild
        player = gameController.getPlayerById(ctx.message.author.name)
        gameController.takeAll(player)
        categories = guild.categories
        channels = []
        display = td.TextDisplay(gameController)
        message = display.outPutTextDisplay()
        for category in categories:
            if category.name == "Players":
                channels = category.channels

        for i in range(len(message)):
            await channels[i].send(f'{message[i]}')
    else:
        ctx.send(
            ":x: Nobody is playing now. If you want to start a game, use ``!start-game``")


@bot.command(name="c", help="Who is the last CareCaca?")
async def carecaca(ctx):
    guild = ctx.guild
    careCaca = gameController.returnCareCaca()
    if careCaca != None:
        categories = guild.categories
        channels = []
        for category in categories:
            if category.name == "Players":
                channels = category.channels

        for i in range(len(channels)):
            await channels[i].send(f'{careCaca.getId()}')
    else:
        return


# adefecio
def valor(arg):
    if arg in ["a", "A"]:
        return 20
    elif arg in ["j", "J"]:
        return 11
    elif arg in ["q", "Q"]:
        return 12
    elif arg in ["k", "K"]:
        return 13
    elif arg in ["jk", "JK", "joker", "Joker"]:
        return 30
    else:
        return arg


bot.run(TOKEN)
