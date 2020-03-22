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

    def equalCard(self, card):
        return self.getValue() == card.getValue()

    def geq(self, card):
        return self.value >= card.value

    def leq(self, card):
        return self.value <= card.value

    def isValidWith(self, card):
        if (self.value in [2, A, JK]):
            return True
        elif(card.value == 7):
            return self.leq(card)
        else:
            return self.geq(card)

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
            return "none"


def deck():
    deck = []
    for k in range(0, 2):
        for i in range(0, 4):
            deck.append(Card(JK, "all"))
            if i == 0:
                suit = "Pica"
            elif i == 1:
                suit = "Clover"
            elif i == 2:
                suit = "Heart"
            elif i == 3:
                suit = "Diamond"
            for j in range(1, 14):
                if j == 1:
                    deck.append(Card(A, suit))
                elif j == 11:
                    deck.append(Card(J, suit))
                elif j == 12:
                    deck.append(Card(Q, suit))
                elif j == 13:
                    deck.append(Card(K, suit))
                else:
                    deck.append(Card(j, suit))
    return deck


def sortedDeck():
    deck_ = deck()
    deck_.sort()
    return deck_
