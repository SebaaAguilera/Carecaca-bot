import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


A = 20
J = 11
Q = 12
K = 13
JK = 30


class ImgDisplay(object):
    def __init__(self, controller, folder="/PNG"):
        self.controller = controller
        self.folder = folder

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
                    im = Image.open(p[1], 'r')
                    fs.append(im)
                elif lenTable < j < m:
                    im = Image.open("PNG/gray_back.png", 'r')
                    fs.append(im)
                elif m <= j < lenHidden:
                    im = Image.open(p[2], 'r')
                    fs.append(im)
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

    def handCards(self, info):


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
