from card import *


class Player(object):
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.visible = []
        self.hiddenTable = []

    def __str__(self):
        return str(self.id)

    def reset(self):
        self.hand = []
        self.visible = []
        self.hiddenTable = []

    def getId(self):
        return self.id

    def equalId(self, player):
        return self.getId() == player.getId()

    def setHand(self, card):
        self.hand.append(card)

    def setManyCardsToHand(self, cards):
        for card in cards:
            self.hand.append(card)

    def getHand(self):
        return self.hand

    def getHandCardByValue(self, cardValue):
        for card in self.hand:
            if card.value == cardValue:
                return card

    def getHandLen(self):
        return len(self.hand)

    def popCardFromHand(self, card):
        # for i in range(0, len(self.hand)):
        #    if card == self.hand[i].getValue():
        # return self.hand.pop(i)
        return self.hand.pop(self.hand.index(card))

    def setVisible(self, card):
        self.visible.append(card)

    def setManyCardsToVisible(self, cards):
        for card in cards:
            self.visible.append(card)

    def getVisible(self):
        return self.visible

    def getVisibleCardByValue(self, cardValue):
        for card in self.visible:
            if card.value == cardValue:
                return card

    def getVisibleLen(self):
        return len(self.visible)

    def popCardFromVisible(self, card):
        # for i in range(0, len(self.visible)):
        #    if card == self.visible[i].getValue():
        #        return self.visible.pop(i)
        return self.visible.pop(self.visible.index(card))

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
        # for i in range(0, len(self.hiddenTable)):
        #    if card == self.hiddenTable[i].getValue():
        #        return self.hiddenTable.pop(i)
        return self.hiddenTable.pop(self.hiddenTable.index(card))

    def hasNoCards(self):
        return self.getHandLen() == 0 and self.getVisibleLen() == 0 and self.getHiddenLen() == 0
