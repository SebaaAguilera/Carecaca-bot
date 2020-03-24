from card import *


class Player(object):
    def __init__(self, id, hand=[], table=[], hiddenTable=[]):
        self.id = id
        self.hand = hand
        self.table = table
        self.hiddenTable = hiddenTable

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

    def hasInTable(self, card):
        for i in range(0, len(self.table)):
            if card == self.table[i].getValue():
                return True
        return False

    def setTable(self, card):
        self.table.append(card)

    def getTable(self):
        return self.table

    def getTableLen(self):
        return len(self.table)

    def popCardFromTable(self, card):
        for i in range(0, len(self.table)):
            if card == self.table[i].getValue():
                return self.table.pop(i)

    def hasInHidden(self, card):
        for i in range(0, len(self.hiddenTable)):
            if card == self.hiddenTable[i].getValue():
                return True
        return False

    def setHiddenCard(self, card):
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
        return self.getHandLen == 0 and self.getTableLen() == 0 and self.getHiddenLen() == 0
