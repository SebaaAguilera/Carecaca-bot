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
        if (self.value in [2, A, JK]):
            return True
        elif(cardValue == 7):
            return self.leq(cardValue)
        else:
            return self.geq(cardValue)

    def returnEffect(self):
        if(self.value == 8):
            return "skip"
        elif (self.value == 10):
            return "burn"
        elif(self.value == J):
            return "changeOrder"
        elif(self.value == JK):
            return "takeAll"
        else:
            return None

    # dispay card


def deck():
    dck = []
    for i in range(0, 3):
        dck.append(Card(JK, "all"))
    for k in range(0, 2):
        for i in range(0, 4):
            if (i == 0):
                suit = "Pica"
            elif (i == 1):
                suit = "Clover"
            elif (i == 2):
                suit = "Heart"
            elif (i == 3):
                suit = "Diamond"
            for j in range(1, 14):
                if (j == 1):
                    dck.append(Card(A, suit))
                elif (j == 11):
                    dck.append(Card(J, suit))
                elif (j == 12):
                    dck.append(Card(Q, suit))
                elif (j == 13):
                    dck.append(Card(K, suit))
                else:
                    dck.append(Card(j, suit))
    return dck


def sortedDeck(d=deck()):
    shuffle(d)
    return d
