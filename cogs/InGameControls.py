from discord.ext import commands
import discord

# Custom
import Models.Card as card
import Models.Player as player
import GameController.GameController as gc
import Display.TextDisplay as td


class InGameControls(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
            await channels[i].send(f'{message[i]}')

    async def requestCtr(self, ctx, functionCall):
        if (functionCall):  # aqui llegaria el putBlablabla
            await self.msgStatus(ctx)
        else:
            await ctx.send(":x: Something went wrong")

    def value(self, arg):
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
            return int(arg)

    @commands.command(name="l", help="You'll leave the game", aliases=['leave'])
    async def l(self, ctx):
        # if gameController.playing:
        authorId = ctx.message.author.guild.id
        ctr = self.bot.gcDict.get(authorId)
        if ctr is not None:
            if len(ctr.getPlayers()) == 1:
                await ctx.send(":x: Are u playing alone?, please use !end-game to end your lonely game dude")
                return
            player = ctr.getPlayerById(ctx.message.author.name)
            if (player.getId() == ctr.getTurnOwner().getId()):
                ctr.endTurn(player)
                await self.msgStatus(ctx)
            ctr.leaveGame(player)
        else:
            await ctx.send(
                ":x: Nobody is playing now. If you want to start a game, use ``!start-game``")

    # !y <cardNumber>
    #
    @commands.command(name="y", help="Put a card from your hand like '!y 5'")
    async def y(self, ctx, *, args):
        # if ctr.playing:
        authorId = ctx.message.author.guild.id
        ctr = self.bot.gcDict.get(authorId)
        if ctr is not None:
            player = ctr.getPlayerById(ctx.message.author.name)
            await self.requestCtr(ctx, ctr.putCardFromHand(player, self.value(args)))
        else:
            await ctx.send(
                ":x: Nobody is playing now. If you want to start a game, use ``!start-game``")

    @commands.command(name="t", help="Put a card from your table cards like '!t J'", aliases=['table'])
    async def t(self, ctx, *, args):
        # if ctr.playing:
        authorId = ctx.message.author.guild.id
        ctr = self.bot.gcDict.get(authorId)
        if ctr is not None:
            player = ctr.getPlayerById(ctx.message.author.name)
            await self.requestCtr(ctx, ctr.putCardFromVisible(player, self.value(args)))
        else:
            await ctx.send(
                ":x: Nobody is playing now. If you want to start a game, use ``!start-game``")

    @commands.command(name="h", help="Put a card from your hidden cards like '!h 2'", aliases=['hidden'])
    async def h(self, ctx, *, args):
        # if ctr.playing:
        authorId = ctx.message.author.guild.id
        ctr = self.bot.gcDict.get(authorId)
        if ctr is not None:
            player = ctr.getPlayerById(ctx.message.author.name)
            await self.requestCtr(ctx, ctr.putCardFromHidden(player, int(args)))
        else:
            await ctx.send(
                ":x: Nobody is playing now. If you want to start a game, use ``!start-game``")

    # list
    @commands.command(name="n", help="If there're not available cards, take all from the table!!'", aliases=['none'])
    async def n(self, ctx):
        # if ctr.playing:
        authorId = ctx.message.author.guild.id
        ctr = self.bot.gcDict.get(authorId)
        if ctr is not None:
            player = ctr.getPlayerById(ctx.message.author.name)
            ctr.takeAll(player)
            await self.msgStatus(ctx)
        else:
            await ctx.send(
                ":x: Nobody is playing now. If you want to start a game, use ``!start-game``")

    @commands.command(name="c", help="Who is the last CareCaca? (not working yet)", aliases=['carecaca'])
    async def carecaca(self, ctx):
        authorId = ctx.message.author.guild.id
        ctr = self.bot.gcDict.get(authorId)
        if ctr is not None:
            guild = ctx.guild
            careCaca = ctr.returnCareCaca()
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


def setup(bot):
    bot.add_cog(InGameControls(bot))
