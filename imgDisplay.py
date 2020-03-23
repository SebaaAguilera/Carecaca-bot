import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


A = 20
J = 11
Q = 12
K = 13
JK = 30


class ImgDisplay(object):
    def __init__(self, bot, controller, folder="/PNG"):
        self.controller = controller
        self.folder = folder
        self.bot = bot

    def getPlayersDisplay(self):
        numOfPlayers = self.controller.getPlen()
        players = self.controller.getPlayers()
        playerInfo = []
        for i in range(0, numOfPlayers):
            player = players[i]
            playerInfo.append(
                [
                    self.cardsDisplay(player.getHand()),
                    self.cardsDisplay(player.getTable()),
                    self.cardsDisplay(player.getHiddenCards(), False)
                ]
            )
        return playerInfo

    def cardsDisplay(self, cards, show=True):
        nc = []
        for i in range(0, len(cards)):
            nc.append(self.cardDisplay(cards[i]))
        return nc

    def cardDisplay(self, card, show=True):
        if (show):
            value = card.getValue()
            suit = card.getSuit()
            name = str(self.folder)
            if (value == A):
                name += "A"
            elif (value == 2):
                name += "2"
            elif (value == 3):
                name += "3"
            elif (value == 4):
                name += "4"
            elif (value == 5):
                name += "5"
            elif (value == 6):
                name += "6"
            elif (value == 7):
                name += "7"
            elif (value == 8):
                name += "8"
            elif (value == 9):
                name += "9"
            elif (value == 10):
                name += "10"
            elif (value == J):
                name += "J"
            elif (value == Q):
                name += "Q"
            elif (value == K):
                name += "K"
            elif (value == JK):
                name += "JK"
            if (suit == "Pica"):
                name += "P"
            elif (suit == "Clover"):
                name += "C"
            elif (suit == "Heart"):
                name += "H"
            elif (suit == "Diamond"):
                name += "D"
            name += ".png"
            return name
        else:
            return "purple_back.png"

    def tableCards(self, info):
        plCards = []
        for i in range(0, self.controller.getPlen()):
            p = info[i]
            lenTable = len(p[1])
            lenHidden = len(p[2])
            m = max(lenTable, lenHidden)
            fs = []
            for j in range(0, 2*m):
                if j <= lenTable:
                    im = Image.open(p[1][j], 'r')
                elif lenTable < j < m:
                    im = Image.open("PNG/gray_back.png", 'r')
                elif m <= j < lenHidden:
                    im = Image.open(p[2][j], 'r')
                else:
                    im = Image.open("PNG/gray_back.png", 'r')
                fs.append(im)
            x, y = fs[0].size
            ncol = 2
            nrow = 2
            cvs = Image.new('RGB', (x*ncol, y*nrow))
            for i in range(len(fs)):
                px, py = x*(i % ncol), y*int(i/ncol)
                cvs.paste(fs[i], (px, py))
            plCards.append(cvs)
            # cvs.show()
        return plCards

    def handCards(self, info):
        plCards = []
        for i in range(0, self.controller.getPlen()):
            p = info[i]
            lenHand = len(p[0])
            fs = []
            resto = lenHand % 3
            if resto == 0:
                resto = 3
            for j in range(0, lenHand+(3-resto)):
                if j >= lenHand:
                    im = Image.open("PNG/gray_back.png", 'r')
                else:
                    im = Image.open(p[0][j], 'r')
                fs.append(im)
            x, y = fs[0].size
            ncol = 3
            nrow = lenHand+(3-resto) / 3
            cvs = Image.new('RGB', (x*ncol, y*nrow))
            for i in range(len(fs)):
                px, py = x*(i % ncol), y*int(i/ncol)
                cvs.paste(fs[i], (px, py))
            plCards.append(cvs)
        return plCards

    def middleCards(self):
        fs = []
        im = Image.open(self.cardDisplay(self.controller.getCardOnTop()), 'r')
        fs.append(im)
        if (self.controller.haveCards()):
            im = Image.open("PNG/purple_back.png", 'r')
            fs.append(im)
            x, y = fs[0].size
            ncol = 2
            nrow = 1
            cvs = Image.new('RGB', (x*ncol, y*nrow))
            for i in range(len(fs)):
                px, py = x*(i % ncol), y*int(i/ncol)
                cvs.paste(fs[i], (px, py))
            return cvs
        else:
            return im

    def outputDisplay(self):
        info = self.getPlayersDisplay()
        tableC = self.tableCards(info)
        handC = self.handCards(info)
        middle = self.middleCards()
        players = self.controller.getPlayers()
        for i in range(0, self.controller.getPlen()):
            for j in range(0, self.controller.getPlen()):
                if i != j:
                    # send name of the cards owner bot.message(players[j].getId() + "'s cards:")
                    # send an image with the cards bot.img(tableC[j])
                    # someHow we'll have to upload the image to discord itself and then send them to the players
                    caca = "uwu"
            # send a msg bot.msg("Cards on the table")
            # send the cards in the middle of the table bot.img(middle)
            # send name of the cards owner bot.message("Your cards:")
            # send an image with the cards in the table bot.img(tableC[i])
            # send an image with the cards in the hand bot.img(hand[i])


def printTest():
    fs = []
    for i in range(2, 6):
        im = Image.open("PNG/"+str(i)+"C.png", 'r')
        fs.append(im)
    x, y = fs[0].size
    ncol = 2
    nrow = 2
    cvs = Image.new('RGB', (x*ncol, y*nrow))
    # for i in range(len(fs)):
    for i in range(len(fs)):
        px, py = x*(i % ncol), y*int(i/ncol)
        cvs.paste(fs[i], (px, py))
    cvs.show()


printTest()
