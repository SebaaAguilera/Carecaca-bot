
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

    # Cards in the stack
    def setCardOnTop(self, card):
        self.cardStack.append(card)
        self.cardOnTop = card

    def getCardOnTop(self):
        return self.cardOnTop

    def burn(self):
        self.cardStack = []

    def getTurnOwner(self):
        return self.turnOwner

    def getPlayers(self):
        return self.players

    def getPlen(self):
        return len(self.players)

    def indexP(self, player):
        return self.players.index(player)

    def addCounter(self, player, card):
        if (card.equalCard(self.getCardOnTop())):
            self.counter += 1
            if (self.counter == 4):
                self.burn()
                self.counter = 0
                return True
        else:
            self.counter = 0

    def putCardOnStack(self, player, card):
        if (isinstance(card, Card)):
            if(card.isValidWith(self.getCardOnTop())):
                if(self.flash):
                    if (card in player.getHand()):
                        self.turnOwner = player
                        self.setCardOnTop(player.popCardFromHand(card))
                    elif (card in player.getTable() and player.getHandLen() == 0):
                        self.turnOwner = player
                        self.setCardOnTop(player.popCardFromTable())
                elif (player.equalId(self.turnOwner)):
                    if (card in player.getHand()):
                        self.setCardOnTop(player.popCardFromHand(card))
                    elif (card in player.getTable() and player.getHandLen() == 0):
                        self.setCardOnTop(player.popCardFromTable())
                if (not self.addCounter(player, card)):
                    self.endTurnEffects(player)
            else:
                # wrong card, take all the stack
                player.setManyCardsToHand(self.cardStack)
                self.cardStack = []
                self.endTurnEffects(player)
        else:
            if (card == 0):
                # have no cards
                player.setManyCardsToHand(self.cardStack)
                self.cardStack = []
                self.endTurnEffects(player)
            elif (player.equalId(self.turnOwner) and player.getHandLen() == 0 and player.getTableLen == 0):
                if (player.getHiddenCards()[card-1].isValidWith(self.getCardOnTop())):
                    self.setCardOnTop(player.popCardFromHidden(card-1))
                    if (not self.addCounter(player, card)):
                        self.endTurnEffects(player)
                else:
                    # wrong card, take all
                    player.setHand(player.popCardFromHidden(card-1))
                    player.setManyCardsToHand(self.cardStack)
                    self.cardStack = []
                    self.endTurnEffects(player)

    def endTurn(self, player, skip=0):
        if (self.order):
            self.turnOwner = self.players[(self.indexP(
                player)+1+skip) % self.getPlen()]
            while(self.turnOwner.hasNoCards()):
                self.turnOwner = self.players[(
                    self.indexP(player)+1) % self.getPlen()]
        else:
            self.turnOwner = self.players[(
                self.indexP(player)-1-skip) % self.getPlen()]
            while(self.turnOwner.hasNoCards()):
                self.turnOwner = self.players[(
                    self.indexP(player)-1) % self.getPlen()]

    def endTurnEffects(self, player):
        effect = self.getCardOnTop().returnEffect()
        if (effect == "skip"):
            self.endTurn(1)
        elif (effect == "burn"):
            self.burn()
        elif (effect == "changeOrder"):
            self.order = not self.order
            self.endTurn(player)
        elif (effect == "takeAll"):
            self.cardStack.pop()
            if(self.order):
                auxPlayer = self.players[self.indexP(
                    player)+1 % self.getPlen()]
                while(auxPlayer.hasNoCards):
                    auxPlayer = self.players[self.indexP(
                        auxPlayer)+1 % self.getPlen()]
                auxPlayer.setManyCardsToHand(self.cardStack)
            else:
                auxPlayer = self.players[self.indexP(
                    player)-1 % self.getPlen()]
                while(auxPlayer.hasNoCards):
                    auxPlayer = self.players[self.indexP(
                        auxPlayer)-1 % self.getPlen()]
                auxPlayer.setManyCardsToHand(self.cardStack)
            self.cardStack = []
            self.endTurn(player, 1)
        else:
            self.endTurn(player)
