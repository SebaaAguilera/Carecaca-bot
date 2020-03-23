
from card import *
from player import *


class GameController(object):
    def __init__(self, players, flash):
        self.players = players
        self.deck = sortedDeck()
        self.cardStack = []
        self.cardOnTop = None
        self.turnOwner = None
        self.order = True  # true: right, false: left
        self.flash = flash
        self.counter = 0

    def initGame(self):
        for player in self.players:
            # Add 3 cards per player in each box
            for i in range(0, 3):
                player.setHand(self.deck.pop())
                player.setTable(self.deck.pop())
                player.setHiddenCard(self.deck.pop())

    def changeOrder(self):
        self.order = not self.order

    def returnOrder(self):
        if(self.order):
            return +1
        else:
            return -1

    # Cards in the stack

    def setCardOnTop(self, player, card):
        self.drawCards(player)
        self.cardStack.append(card)
        self.cardOnTop = card

    def getCardOnTop(self):
        return self.cardOnTop

    def getAllFromStack(self, player):
        player.setManyCardsToHand(self.cardStack)
        self.cardStack = []
        self.cardOnTop = None

    def haveCards(self):
        return len(self.deck) > 0

    def burn(self):
        self.cardStack = []

    def drawCards(self, player):
        while (len(self.deck) > 0 and player.getHandLen() < 3):
            player.setHand(self.deck.pop())

    def getTurnOwner(self):
        return self.turnOwner

    def getPlayers(self):
        return self.players

    def getPlen(self):
        return len(self.players)

    def indexP(self, player):
        return self.players.index(player)

    def addCounter(self, player, card):
        if (card.equalValue(self.getCardOnTop())):
            self.counter += 1
            if (self.counter == 4):
                self.burn()
                self.counter = 0
                return True
        else:
            self.counter = 0

    def pCOS_True(self, player, card):
        if(card.isValidWith(self.getCardOnTop())):
            if(self.flash and card.equalValue(self.cardOnTop)):
                if (card in player.getHand()):
                    self.turnOwner = player
                    self.setCardOnTop(player, player.popCardFromHand(card))
                elif (card in player.getTable() and player.getHandLen() == 0):
                    self.turnOwner = player
                    self.setCardOnTop(player, player.popCardFromTable())
            elif (player.equalId(self.turnOwner) and not self.flash):
                if (card in player.getHand()):
                    self.setCardOnTop(player, player.popCardFromHand(card))
                elif (card in player.getTable() and player.getHandLen() == 0):
                    self.setCardOnTop(player, player.popCardFromTable())
            # not valid player
            else:
                self.getAllFromStack(player)
            if (not self.addCounter(player, card)):
                self.endTurnEffects(player)
        else:
            # wrong card, take all the stack
            self.getAllFromStack(player)
            self.endTurn(player)

    def pCOS_False(self, player, card):
        if (card == 0):
            # have no cards
            self.getAllFromStack(player)
            self.endTurn(player)
        elif (player.equalId(self.turnOwner) and player.getHandLen() == 0 and player.getTableLen == 0):
            if (player.getHiddenCards()[card % 10 - 1].isValidWith(self.getCardOnTop())):
                self.setCardOnTop(
                    player, player.popCardFromHidden(card % 10 - 1))
                if (not self.addCounter(player, card)):
                    self.endTurnEffects(player)
            else:
                # wrong card, take all
                player.setHand(player.popCardFromHidden(card % 10 - 1))
                self.getAllFromStack(player)
                self.endTurn(player)

    def putCardOnStack(self, player, card):
        if (isinstance(card, Card)):  # atenzao con esto
            self.pCOS_True(player, card)
        else:
            self.pCOS_False(player, card)

    def returnPlayer_Order(self, player, skip=0):
        return self.players[(self.indexP(
            player)+self.returnOrder()*(1+skip)) % self.getPlen()]

    def endTurn(self, player, skip=0):
        auxPlayer = self.returnPlayer_Order(player, skip)
        while(auxPlayer.hasNoCards()):
            auxPlayer = self.returnPlayer_Order(auxPlayer)
        self.turnOwner = auxPlayer

    def endTurnEffects(self, player):
        effect = self.getCardOnTop().returnEffect()
        if (effect == "skip"):
            self.endTurn(1)
        elif (effect == "burn"):
            self.burn()
        elif (effect == "changeOrder"):
            self.changeOrder()
            self.endTurn(player)
        elif (effect == "takeAll"):
            self.cardStack.pop()
            auxPlayer = self.returnPlayer_Order(player)
            while(auxPlayer.hasNoCards):
                auxPlayer = self.returnPlayer_Order(auxPlayer)
            self.getAllFromStack(auxPlayer)
            self.endTurn(auxPlayer)  # posiblemente de error
        else:
            self.endTurn(player)

    def returnCareCaca(self):
        if (self.getPlen() == 1):
            return self.players[0]
        else:
            return None
