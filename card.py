from random import shuffle

A = 20
J = 11
Q = 12
K = 13
JK = 30


class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return str(self.value) + " " + str(self.suit)

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit

    def equalValue(self, card):
        return self.getValue() == card.getValue()

    def equalSuit(self, card):
        return self.suit == card.suit

    def equalCard(self, card):
        return self.equalValue(card) and self.equalSuit(card)

    def geq(self, card):
        return self.value >= card.getValue()

    def leq(self, card):
        return self.value <= card.getValue()

    def isValidWith(self, card):
        if self.value in [2, A, JK] or card is None:
            return True
        elif(card.getValue() == 7):
            return self.leq(card)
        else:
            return self.geq(card)

    def returnEffect(self):
        if (self.value == 2):
            return None
        elif(self.value == 8):
            return "skip"
        elif (self.value == 10):
            return "burn"
        elif(self.value == J):
            return "changeOrder"
        elif(self.value == JK):
            return "takeAll"
        else:
            return None
