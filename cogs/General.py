from discord.ext import commands

import discord

# Custom
import Models.Card as card
import Models.Player as player
import GameController.GameController as gc
import Display.TextDisplay as td


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hi", help="Say Hi to CareCaca bot!")
    async def hi(self, ctx):
        await ctx.send(f'Hi {ctx.message.author.name}, nice to meet you! :heart:')

    @commands.command(name="get-players", help="Print currently players (???")
    async def get_players(self, ctx):
        ctr = self.bot.gcDict.get(ctx.message.author.guild.id)
        players = ctr.getPlayers()
        string = ""
        for player in players:
            string += player.getId() + "\n"
        e = discord.Embed(title=f'{string}')
        await ctx.send(f"Jugadores conectados: \n", embed=e)


def setup(bot):
    bot.add_cog(General(bot))
