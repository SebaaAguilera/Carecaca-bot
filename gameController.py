
from card import *
from player import *
from deck import *


class GameController(object):
    def __init__(self):
        self.playing = False
        self.players = []
        self.deck = Deck(True)
        self.cardStack = []
        self.cardOnTop = None
        self.turnOwner = None
        self.order = True  # true: right, false: left
        self.flash = False
        self.counter = 0

    def resetController(self):
        self.playing = False
        self.resetPlayers()
        self.players = []
        self.deck = Deck(True)
        self.cardStack = []
        self.cardOnTop = None
        self.turnOwner = None
        self.order = True  # true: right, false: left
        self.flash = False
        self.counter = 0

    def resetPlayers(self):
        [player.reset() for player in self.players]

    def setPlayer(self, player):
        self.players.append(player)

    def setFlash(self, flash):
        self.flash = flash

    def initGame(self):
        for player in self.players:
            player.setManyCardsToHand(self.deck.popAListByLen(3))
            player.setManyCardsToVisible(self.deck.popAListByLen(3))
            player.setManyCardsToHidden(self.deck.popAListByLen(3))
        self.turnOwner = self.players[0]
        self.playing = True

    def getStatus(self):
        return [self.cardOnTop, self.turnOwner, self.order]

    def compareStatus(self, prevStatus):
        newSt = self.getStatus()
        for st in newSt:
            if st is not prevStatus[newSt.index(st)]:
                return True
        return False

    def changeDeck(self, deck):
        self.deck = deck

    def getOrder(self):
        return self.order

    def changeOrder(self):
        self.order = not self.order

    def returnOrder(self):
        if(self.order):
            return +1
        else:
            return -1

    # Cards in the stack

    def setCardOnTop(self, player, card):
        self.addCounter(player, card)
        self.cardStack.append(card)
        self.cardOnTop = card
        self.drawCards(player)
        self.endTurnEffects(player)

    def getCardOnTop(self):
        return self.cardOnTop

    def getStack(self):
        return self.cardStack

    def getAllFromStack(self, player):
        player.setManyCardsToHand(self.cardStack)
        self.cardStack = []
        self.cardOnTop = None
        self.counter = 0

    def haveCards(self):
        return self.deck.len() > 0

    def burn(self):
        self.cardOnTop = None
        self.cardStack = []
        self.counter = 0

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
            if player.getId() is id:
                return player

    def getPlen(self):
        return len(self.players)

    def indexP(self, player):
        return self.players.index(player)

    def addCounter(self, player, card):
        if self.cardOnTop is None or self.cardOnTop.equalValue(card):
            self.counter += 1
        else:
            self.counter = 0

    def getCounter(self):
        return self.counter

    def putCardAbstract(self, player, card, hand=True, emptyHand=True):
        if card is None:
            return False
        prevStatus = self.getStatus()
        if(card.isValidWith(self.getCardOnTop())):
            if (self.flash and card.equalValue(self.cardOnTop)) or player.equalId(self.turnOwner):
                self.turnOwner = player
                if hand:
                    self.setCardOnTop(
                        player, player.popCardFromHand(card))
                elif emptyHand:
                    self.setCardOnTop(
                        player, player.popCardFromVisible(card))
                # if he/she don't own the card: do nothing
            # not valid player
            else:
                self.getAllFromStack(player)
        else:
            # wrong card, take all the stack
            self.getAllFromStack(player)
            self.endTurn(player)
        return self.compareStatus(prevStatus)

    # command !p (card number)
    def putCardFromHand(self, player, cardValue):
        return self.putCardAbstract(player, player.getHandCardByValue(cardValue))

    # command !t (card value)
    def putCardFromVisible(self, player, cardValue):
        return self.putCardAbstract(player, player.getVisibleCardByValue(cardValue), False, player.getHandLen() == 0)

    # command !h (card number)
    def putCardFromHidden(self, player, cardIndex):
        prevStatus = self.getStatus()
        if cardIndex not in range(1, player.getHiddenLen()+1):
            return False
        card = player.getHidden()[cardIndex - 1]
        if (player.equalId(self.turnOwner) and player.getHandLen() == 0 and player.getVisibleLen == 0):
            if card.isValidWith(self.cardOnTop):
                self.setCardOnTop(
                    player, player.popCardFromHidden(card))
                self.endTurnEffects(player)
            else:
                # wrong card, take all
                player.setHand(player.popCardFromHidden(card))
                self.getAllFromStack(player)
                self.endTurn(player)
        return self.compareStatus(prevStatus)

    # command !n
    def takeAll(self, player):
        if player.equalId(self.turnOwner):
            self.getAllFromStack(player)
            self.endTurn(player)

    def returnPlayer_Order(self, player, skip=0):
        return self.players[(self.indexP(player)+self.returnOrder()*(1+skip)) % self.getPlen()]

    def endTurn(self, player, skip=0):
        auxPlayer = self.returnPlayer_Order(player, skip)
        while(auxPlayer.hasNoCards()):
            auxPlayer = self.returnPlayer_Order(auxPlayer)
        self.turnOwner = auxPlayer

    def endTurnEffects(self, player):
        if self.cardOnTop is None:
            self.endTurn(player)
            return
        effect = self.getCardOnTop().returnEffect()
        if (effect == "skip"):
            self.endTurn(player, 1)
        elif (effect == "burn" or self.counter == 4):
            self.burn()
        elif (effect == "changeOrder"):
            self.changeOrder()
            self.endTurn(player)
        elif (effect == "takeAll"):
            self.cardStack.pop()
            auxPlayer = self.returnPlayer_Order(player)
            while(auxPlayer.hasNoCards()):
                print(auxPlayer)
                auxPlayer = self.returnPlayer_Order(auxPlayer)
            self.getAllFromStack(auxPlayer)
            self.endTurn(auxPlayer)  # posiblemente de error
        else:
            self.endTurn(player)

    def returnCareCaca(self):
        playersLeft = []
        for player in self.players:
            if player.hasNoCards():
                playersLeft.append(player)
        if len(playersLeft) == 1:
            return playersLeft[0]
        else:
            return None
