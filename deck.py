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

    def popCardByValue(self, cardValue):
        for i in range(0, 108):
            if cardValue == self.get(i).getValue():
                # , print("pop para los h " + str(dck.len()))
                return self.pop(i)

    def initDeck(self):
        for i in range(0, 4):
            self.deck.append(Card(JK, "all"))
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
                        self.deck.append(Card(A, suit))
                    elif (j == 11):
                        self.deck.append(Card(J, suit))
                    elif (j == 12):
                        self.deck.append(Card(Q, suit))
                    elif (j == 13):
                        self.deck.append(Card(K, suit))
                    else:
                        self.deck.append(Card(j, suit))

    def sortDeck(self):
        shuffle(self.deck)
