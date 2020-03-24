# bot.py
import os

import discord
import logging
from discord import Role
from dotenv import load_dotenv
from discord.ext import commands
import card
import player

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
    
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
# add_role_to_player
# role_name:str player: discord.Guild.member obj
# Add role to Player
async def add_role_to_player(role_name, player):
    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        print(f'Adding role: {role_name} to {player.name}')
        await player.add_roles(role)
        await print(f'Role {role_name} has been asigment to {player.name}')

# create_new_role
# guild: discord.Guild role_name: str **kargs: args
# Create a new role
async def create_new_role(guild: discord.Guild, role_name: str, **kargs) -> Role:
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if not existing_role:
        print(f'Creating a new role: {role_name}')
        new_role = await guild.create_role(name=role_name, **kargs)
        await print(f'Role {new_role.name} has been created successfuly')
        return new_role
    else:
        await existing_role.edit(**kargs)
        print(f'Role {role_name} already exists!')
        return existing_role

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
async def startGame(ctx):
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
            await create_new_role(guild, role_name, mentionable=True, colour=discord.Colour(0x09c48c))
            await add_role_to_player(role_name, members[i])
            await manage_text_channel(ctx, channel_name, "add", main_category)
            await set_permission_text_channel(ctx, channel_name, role_name, main_category)
    
    await ctx.send('Room is ready, please join to your Text Channel')
        

@bot.command(name="end-game", help="End a CareCaca game")
async def endGame(ctx):
    await ctx.send(f'{ctx.message.author.name} has ended the game')
    await ctx.send('Deleting room...')
    guild = ctx.guild
    members = ctx.message.guild.members
    category = discord.utils.get(guild.categories, name="Players")

    # Deleting Roles
    for i in range(len(members)):
        if members[i].name =="Carecaca-bot":
            continue
        if members[i].status != discord.Status.offline:
            role_name = "player-" + str(i) 
            channel_name = role_name
            await delete_role(ctx, role_name)
            await manage_text_channel(ctx, channel_name, "remove", category)
            
    # Deleting category 'Players'  
    await category.delete(reason="End game")

    await ctx.send('Room has been deleted')

@bot.command(name="emoji", help="testing emoji messages")
async def emoji(ctx):
    await ctx.send(':regional_indicator_a:')

    await ctx.send('Room was delete')


bot.run(TOKEN)
