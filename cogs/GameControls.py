from discord.ext import commands

import discord
from discord import Role

# Custom
import Models.Card as card
import Models.Player as player
import GameController.GameController as gc
import Display.TextDisplay as td


class GameControls(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def create_new_role(self, guild: discord.Guild, role_name: str, **kargs) -> Role:
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if not existing_role:
            print(f'Creating a new role: {role_name}')
            new_role = await guild.create_role(name=role_name, **kargs)
            return new_role
        else:
            await existing_role.edit(**kargs)
            return None

    async def create_role(self, ctx, member, guild: discord.Guild, role_name: str, **kargs):
        role = await self.create_new_role(guild, role_name, mentionable=True, colour=discord.Colour(0x09c48c))
        if role != None:
            print(f'Role {role.name} has been created successfuly')
            await self.add_role_to_player(ctx, role, member)
        else:
            print(f'Role {role_name} already exists!')

    # add_role_to_player
    # role_name:str member: discord.Guild.member obj
    # Add role to Player

    async def add_role_to_player(self, ctx, role, member):
        print(f'Adding role: {role.name} to {member.name}')
        await member.add_roles(role)
        print(f'Role {role.name} has been asigment to {member.name}')
        await self.asign_member_to_object_player(member)

    # assign_member_to_object_player
    # role: discord.Role obj
    # Connect Player objecto to Member with Role Member.

    async def asign_member_to_object_player(self, member):
        pl = player.Player(member.name)
        print(f'Object player {pl.getId()} has been assigned to {member.name}')
        # gameController.setPlayer(pl)
        self.bot.gcDict[member.guild.id].setPlayer(pl)

    # delete_role
    # ctx:obj role_name:str
    # Delete an existing role

    async def delete_role(self, ctx, role_name):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            print(f'Deleting role: {role.name}')
            await role.delete()

    # manage_text_channel
    # ctx:obj channel_name:str status:str category:discord.Category
    # Can create and remove channel (depends of status)

    async def manage_text_channel(self, ctx, channel_name, status, category):
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

    async def set_permission_text_channel(self, ctx, channel_name, role_name, category):
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

    async def msgStatus(self, ctx):
        guild = ctx.guild
        display = td.TextDisplay(self.bot.gcDict.get(guild.id))
        categories = guild.categories
        channels = []
        message = display.outPutTextDisplay()
        for category in categories:
            if category.name == "Players":
                channels = category.channels
        for i in range(len(message)):
            msg_embed = discord.Embed(
                title="**Game Status:**",
                type="rich",
                description=f"{message[i]}",
                colour=discord.Colour(0x09c48c))
            await channels[i].send(content='', embed=msg_embed, delete_after=300)

    @commands.command(name="start-game", help="Start a CareCaca game")
    async def startGame(self, ctx, *args):
        voice = ctx.message.author.voice
        if voice == None:
            await ctx.send(':x: You must to be in a Voice Channel')
            return
        # if not gameController.playing:
        authorId = ctx.message.author.guild.id
        if self.bot.gcDict.get(authorId) is None:
            self.bot.gcDict[authorId] = gc.GameController()
            ctr = self.bot.gcDict.get(authorId)
            print(self.bot.gcDict)
            if len(args) > 0:
                if args[0] == "True":
                    ctr.setFlash(True)
                elif args[0] == "False":
                    ctr.setFlash(False)
                else:
                    e = discord.Embed(
                        title=':x: Invalid argument, if you wanna play with Flash use ``!start-game True``', colour=discord.Colour(0xff3232))
                    await ctx.send("", embed=e)
                    return

            await ctx.send(f'{ctx.message.author.name} has started a Carecaca Game')
            await ctx.send("Preparing room...")
            # members = ctx.message.guild.members
            guild = ctx.guild

            # Text Channels will agrupate in category 'Players'
            main_category = await guild.create_category_channel("Players")

            # Get the people in a voice channel and server id
            voice_channel = voice.channel
            members = voice_channel.members

            # Creating roles and assigm them to Player
            index = 0
            playersMsg = ""
            for member in members:
                if member.name == "Carecaca-bot":
                    continue
                # if member.status != discord.Status.offline:
                else:
                    index += 1
                    role_name = "player-" + str(index)
                    playersMsg += str(role_name) + ": " + \
                        str(member.name) + "\n"
                    channel_name = role_name
                    await self.create_role(ctx, member, guild, role_name, mentionable=True, colour=discord.Colour(0x09c48c))
                    await self.manage_text_channel(ctx, channel_name, "add", main_category)
                    await self.set_permission_text_channel(ctx, channel_name, role_name, main_category)

            e = discord.Embed(title=':white_check_mark: Room is ready, please join to your Text Channel\n' + 'Assigned rooms: \n' + playersMsg,
                              colour=discord.Colour(0x09c48c))
            await ctx.send('', embed=e)

            # gameController.initGame()
            ctr.initGame()
            await self.msgStatus(ctx)
        else:
            await ctx.send(':x: There is a game already')

    @commands.command(name="end-game", help="End a CareCaca game")
    async def endGame(self, ctx):
        await ctx.send(f'{ctx.message.author.name} has ended the game')
        await ctx.send('Deleting room...')

        server_id = ctx.message.author.guild.id
        ctr = self.bot.gcDict.get(server_id)
        ctr.resetController()

        del self.bot.gcDict[server_id]
        print(self.bot.gcDict)
        guild = ctx.guild
        # members = ctx.message.guild.members
        category = discord.utils.get(guild.categories, name="Players")

        # Get the people in a voice channel
        voice_channel = ctx.message.author.voice.channel
        members = voice_channel.members

        # Deleting Roles
        index = 0
        for member in members:
            if member.name == "Carecaca-bot":
                continue
            else:
                index += 1
                role_name = "player-" + str(index)
                channel_name = role_name
                await self.delete_role(ctx, role_name)
                await self.manage_text_channel(ctx, channel_name, "remove", category)

        # Deleting category 'Players'
        await category.delete(reason="End game")

        


def setup(bot):
    bot.add_cog(GameControls(bot))
