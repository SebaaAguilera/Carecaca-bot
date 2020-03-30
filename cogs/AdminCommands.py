from discord.ext import commands
from discord.ext.commands import CheckFailure, Cog

import discord


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.author.id in self.bot.ADMIN_LIST

    @commands.command(pass_context=True)
    async def broadcast(self, ctx, *, msg):
        for servers in self.bot.guilds:
            for channel in servers.text_channels:
                if "player" in channel.name:
                    await channel.send(f'{msg}')

    @broadcast.error
    async def broadcast_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':x: **Sorry bro, you are not aloud to do that**')

    @commands.command(name="clear", help="Clear text channel")
    async def clear(self, ctx, amount=100):
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=amount):
            messages.append(message)
        await channel.delete_messages(messages)
        await ctx.send(f'{len(messages)} messages deleted by {ctx.message.author.name}.')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':x: **Sorry bro, you are not aloud to do that**')

    @commands.command(name="server-list", help="Obtain servers id's in the case an user needs assitance")
    async def serverList(self, ctx):  # no se que pasa acaaaaaaaaaaaaaaaaa
        servList = "**Server name: id: hasGC** \n"
        for guild in self.bot.guilds:
            servlist += guild.name + ": " + guild.id + ": " + \
                hasGameController(self, guild.id) + "\n"
        servList += "len: " + len(self.bot.guilds)
        print(f'{servList}')
        await ctx.send(f'{servList}')

    @serverList.error
    async def serverList_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':x: **Sorry bro, you are not aloud to do that**')

    @commands.command(name="delete-gc", help="Delete a game using a server id")
    async def delete_gc(self, ctx, *, args):
        # esto se iene que haer de otra forma pero no se como
        del self.bot.gcDict[int(args)]
        if self.bot.gcDict.get(int(args)) is None:
            await ctx.send("Game succesfully deleted")

    @serverList.error
    async def delete_gc_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':x: **Sorry bro, you are not aloud to do that**')


def hasGameController(bot, id):
    return bot.get(id) is not None


def setup(bot):
    bot.add_cog(AdminCommands(bot))
