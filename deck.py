from card import *


class Deck(object):
    def __init__(self, sorted):
        self.deck = []
        self.initDeck()
        if sorted:
            self.sortDeck()

    def pop(self, index=-1):
        return self.deck.pop(index)

    def len(self):
        return len(self.deck)

    def get(self, index):
        return self.deck[index]

    def initDeck(self):
        dck = []
        for i in range(0, 4):
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
        self.deck = dck

    def sortDeck(self):
        shuffle(self.deck)
