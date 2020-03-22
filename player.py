from card import *


class Player(object):
    def __init__(self, id, hand, table, hiddenTable):
        self.id = id
        self.hand = hand
        self.table = table
        self.hiddenTable = hiddenTable

    def getId(self):
        return id

    def equalId(self, player):
        return self.getId() == player.getId()

    def setHand(self, card):
        self.hand.append(card)

    def setManyCardsToHand(self, cards):
        self.hand += cards

    def getHand(self):
        return self.hand

    def getHandLen(self):
        return len(self.hand)

    def popCardFromHand(self, card):
        return self.hand.pop(self.hand.index(card))

    def setTable(self, card):
        self.hand.table(card)

    def getTable(self):
        return self.table

    def getTableLen(self):
        return len(self.table)

    def popCardFromTable(self, card):
        return self.hand.pop(self.table.index(card))

    def setHiddenCard(self, card):
        self.hiddenTable.append(card)

    def getHiddenCards(self):
        return self.hiddenTable

    def getHiddenLen(self):
        return len(self.hiddenTable)

    def popCardFromHidden(self, index):
        return self.hand.pop(index)

    def hasNoCards(self):
        return self.getHandLen == 0 and self.getTableLen() == 0 and self.getHiddenLen() == 0
