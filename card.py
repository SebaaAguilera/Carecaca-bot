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

    def geq(self, cardValue):
        return self.value >= cardValue

    def leq(self, cardValue):
        return self.value <= cardValue

    def isValidWith(self, cardValue):
        if cardValue in [2, A, JK]:
            return True
        elif(self.getValue == 7):
            return self.geq(cardValue)
        else:
            return self.leq(cardValue)

        """
        if (self.value in [2, A, JK]):
            return True
        elif(cardValue == 7):
            return self.leq(7)
        else:
            return self.geq(cardValue)"""

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
