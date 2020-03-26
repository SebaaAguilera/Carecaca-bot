
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
                return False
        return True

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
        self.drawCards(player)
        self.cardStack.append(card)
        self.cardOnTop = card

    def getCardOnTop(self):
        return self.cardOnTop

    def getStack(self):
        return self.cardStack

    def getAllFromStack(self, player):
        player.setManyCardsToHand(self.cardStack)
        self.cardStack = []
        self.cardOnTop = None

    def invalidMove(self, player):
        self.getAllFromStack(player)
        self.addCounter()

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
            if player.getId() is id:
                return player

    def getPlen(self):
        return len(self.players)

    def indexP(self, player):
        return self.players.index(player)

    def addCounter(self, cardValue=0):
        if cardValue == 0:
            self.counter = 0
            # elif self.cardOnTop is None:
            #    self.counter = 1
            return False
        elif (cardValue == self.cardOnTop.getValue()):
            self.counter += 1
            if (self.counter == 4):
                self.burn()
                self.counter = 0
                return True
        else:
            self.counter = 0
            return False

    def getCounter(self):
        return self.counter

    def putCardAbstract(self, player, cardValue, hasInPlace, handOrEmptyHand=True, hand=True):
        prevStatus = self.getStatus()
        print("prevST: ")
        print(prevStatus)
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
                        if (not self.addCounter(cardValue)):
                            self.endTurnEffects(player)
                # if he/she don't own the card: do nothing
            # not valid player
            else:
                print("jugador invalido(?)")
                self.invalidMove(player)
        else:
            print("carta erronea")
            # wrong card, take all the stack
            self.invalidMove(player)
            self.endTurn(player)

        print("newStatus")
        print(self.compareStatus(prevStatus))
        return self.compareStatus(prevStatus)

    # command !p (card number)
    def putCardFromHand(self, player, cardValue):
        print("llamo al abstract")
        return self.putCardAbstract(player, cardValue, player.hasInHand(cardValue))

    # command !t (card value)
    def putCardFromVisible(self, player, cardValue):
        return self.putCardAbstract(player, cardValue, player.hasInVisible(
            cardValue), player.getHandLen() == 0, False)

    # command !h (card number)
    def putCardFromHidden(self, player, cardValue):
        prevStatus = self.getStatus()
        if (player.equalId(self.turnOwner) and player.getHandLen() == 0 and player.getVisibleLen == 0):
            if (player.getHidden()[cardValue - 1].isValidWith(self.getCardOnTop().getValue())):
                self.setCardOnTop(
                    player, player.popCardFromHidden(cardValue - 1))
                if (not self.addCounter(cardValue)):
                    self.endTurnEffects(player)
            else:
                # wrong card, take all
                player.setHand(player.popCardFromHidden(cardValue - 1))
                self.invalidMove(player)
                self.endTurn(player)
        return self.compareStatus(prevStatus)

    # command !n
    def takeAll(self, player):
        if player.equalId(self.turnOwner):
            self.invalidMove(player)
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
        if self.cardOnTop is None:
            self.endTurn(player)
        effect = self.getCardOnTop().returnEffect()
        if (effect == "skip"):
            self.endTurn(1)
        elif (effect == "burn"):
            self.burn()
            self.addCounter()
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
