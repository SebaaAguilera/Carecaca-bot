
from card import *
from player import *
from deck import *


class GameController(object):
    def __init__(self, players, flash):
        self.players = players
        self.deck = Deck(True)
        self.cardStack = []
        self.cardOnTop = None
        self.turnOwner = None
        self.order = True  # true: right, false: left
        self.flash = flash
        self.counter = 0

    def changeDeck(self, deck):
        self.deck = deck

    def initGame(self):
        for player in self.players:
            # Add 3 cards per player in each box
            while(len(player.getHand()) < 3):
                player.setHand(self.deck.pop())
                player.setVisible(self.deck.pop())
                player.setHiddenCard(self.deck.pop())
        self.turnOwner = self.players[0]

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
        return self.deck.len() > 0

    def burn(self):
        self.cardStack = []
        self.cardOnTop = None

    def drawCards(self, player):
        while (self.haveCards() and player.getHandLen() < 3):
            player.setHand(self.deck.pop())

    def getTurnOwner(self):
        return self.turnOwner

    def setTurnOwner(self, player):
        self.turnOwner = player

    def getPlayers(self):
        return self.players

    def getPlayerById(self, id):
        for player in self.players:
            if player.getId() == id:
                return player

    def getPlen(self):
        return len(self.players)

    def indexP(self, player):
        return self.players.index(player)

    def addCounter(self, player, cardValue):
        if self.cardOnTop == None:
            self.counter = 0
            return False
        elif (cardValue == self.cardOnTop().getValue()):
            self.counter += 1
            if (self.counter == 4):
                self.burn()
                self.counter = 0
                return True
        else:
            self.counter = 0
            return False

    def putCardAbstract(self, player, cardValue, hasInPlace, handOrEmptyHand=True, hand=True):
        if(self.getCardOnTop() == None or self.getCardOnTop().isValidWith(cardValue)):
            if(self.flash and cardValue == self.cardOnTop.getValue()) or player.equalId(self.turnOwner):
                if hasInPlace:
                    if handOrEmptyHand:
                        self.turnOwner = player
                        if hand:
                            card = player.popCardFromHand(cardValue)
                        else:
                            card = player.popCardFromVisible(cardValue)
                        self.setCardOnTop(player, card)
                        if (not self.addCounter(player, cardValue)):
                            self.endTurnEffects(player)
                # if he/she don't own the card: do nothing
            # not valid player
            else:
                self.getAllFromStack(player)
                self.endTurn(player)
        else:
            # wrong card, take all the stack
            self.getAllFromStack(player)
            self.endTurn(player)

    # command !p (card number)
    def putCardFromHand(self, player, cardValue):
        self.putCardAbstract(player, cardValue, player.hasInHand(cardValue))

    # command !t (card value)
    def putCardFromVisible(self, player, cardValue):
        self.putCardAbstract(player, cardValue, player.hasInVisible(
            cardValue), player.getHandLen() == 0, False)

    # command !h (card number)
    def putCardFromHidden(self, player, cardValue):
        if (cardValue == 0 and (player.equalId(self.turnOwner))):
            # have no cards
            self.getAllFromStack(player)
            self.endTurn(player)

        if (player.equalId(self.turnOwner) and player.getHandLen() == 0 and player.getVisibleLen == 0):
            if (player.getHidden()[cardValue % 10 - 1].isValidWith(self.getCardOnTop().getValue())):
                self.setCardOnTop(
                    player, player.popCardFromHidden(cardValue % 10 - 1))
                if (not self.addCounter(player, cardValue)):
                    self.endTurnEffects(player)
            else:
                # wrong card, take all
                player.setHand(player.popCardFromHidden(cardValue % 10 - 1))
                self.getAllFromStack(player)
                self.endTurn(player)

    # command !n
    def takeAll(self, player):
        if player.equalId(self.turnOwner):
            self.getAllFromStack()
            self.endTurn(player)

    def returnPlayer_Order(self, player, skip=0):
        return self.players[(self.indexP(
            player)+self.returnOrder()*(1+skip)) % self.getPlen()]

    def endTurn(self, player, skip=0):
        auxPlayer = self.returnPlayer_Order(player, skip)
        while(auxPlayer.hasNoCards()):
            auxPlayer = self.returnPlayer_Order(auxPlayer)
        self.turnOwner = auxPlayer

    def endTurnEffects(self, player):
        # maybe i should apply null pattern here
        if self.cardOnTop == None:
            self.endTurn(player)
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
