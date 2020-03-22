A=20
J=11
Q=12
K=13
JK=30

class Card(object):
    def __init__(self, name, value, suit):
        self.name = name
        self.value = value
        self.suit = suit

    def getValue(self):
        return self.value

    def geq(self, card):
        return self.value >= card.value

    def leq(self, card):
        return self.value <= card.value

    def isValidWith(self,card):
        if (self.value in [2,A,JK]): return True
        elif(card.value==7): return self.leq(card)
        else: return self.geq(card)

    def returnEffect(self):
        if(self.value==8): "skip"
        elif (self.value==10): "burn" 
        elif(self.value==J): "changeOrder"
        elif(self.value==JK):"takeAll"
        else: "none"


def deck():
    deck = []
    for i in range(0, 4):
        deck.append("JK", 30, "all")
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
                deck.append(Card("A", 20, suit))
            elif j == 11:
                deck.append(Card("J", j, suit))
            elif j == 12:
                deck.append(Card("Q", j, suit))
            elif j == 13:
                deck.append(Card("K", j, suit))
            else:
                deck.append(Card(str(j), j, suit))
    return deck
