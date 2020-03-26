from card import *


class Player(object):
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.visible = []
        self.hiddenTable = []

    def reset(self):
        self.hand = []
        self.visible = []
        self.hiddenTable = []

    def getId(self):
        return self.id

    def equalId(self, player):
        return self.getId() == player.getId()

    def hasInHand(self, card):
        for i in range(0, len(self.hand)):
            if card == self.hand[i].getValue():
                return True
        return False

    def setHand(self, card):
        self.hand.append(card)

    def setManyCardsToHand(self, cards):
        for card in cards:
            self.hand.append(card)

    def getHand(self):
        return self.hand

    def getHandLen(self):
        return len(self.hand)

    def popCardFromHand(self, card):
        for i in range(0, len(self.hand)):
            if card == self.hand[i].getValue():
                return self.hand.pop(i)

    def hasInVisible(self, card):
        for i in range(0, len(self.visible)):
            if card == self.visible[i].getValue():
                return True
        return False

    def setVisible(self, card):
        self.visible.append(card)

    def setManyCardsToVisible(self, cards):
        for card in cards:
            self.visible.append(card)

    def getVisible(self):
        return self.visible

    def getVisibleLen(self):
        return len(self.visible)

    def popCardFromVisible(self, card):
        for i in range(0, len(self.visible)):
            if card == self.visible[i].getValue():
                return self.visible.pop(i)

    def hasInHidden(self, cardValue):
        for i in range(0, len(self.hiddenTable)):
            if cardValue == self.hiddenTable[i].getValue():
                return True
        return False

    def setHiddenCard(self, card):
        self.hiddenTable.append(card)

    def setManyCardsToHidden(self, cards):
        for card in cards:
            self.hiddenTable.append(card)

    def getHidden(self):
        return self.hiddenTable

    def getHiddenLen(self):
        return len(self.hiddenTable)

    def popCardFromHidden(self, card):
        for i in range(0, len(self.hiddenTable)):
            if card == self.hiddenTable[i].getValue():
                return self.hiddenTable.pop(i)

    def hasNoCards(self):
        return self.getHandLen == 0 and self.getVisibleLen() == 0 and self.getHiddenLen() == 0
