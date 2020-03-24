from gameController import *
from player import *
from card import *
from deck import *

A = 20
J = 11
Q = 12
K = 13
JK = 30

# Test without flash

dck = Deck(True)
print(dck.len())


def returnList(deck, cardList):
    x = []
    for cardValue in cardList:
        x.append(deck.popCardByValue(cardValue))
    return x


# setHands
h0 = returnList(dck, [A, JK, 6])
h1 = returnList(dck, [6, 10, J])
h2 = returnList(dck, [6, 7, 8])
h3 = returnList(dck, [6, 7, 2])


# setPlayers
p0 = Player(0, h0)
p1 = Player(1, h1)
p2 = Player(2, h2)
p3 = Player(3, h3)

pl = [p0, p1, p2, p3]

# setGameController
ctr = GameController(pl, False)
ctr.changeDeck(dck)

# set visible and hidden visibleCards
for player in ctr.getPlayers():
    # Add 3 cards per player in each box
    while(len(player.getVisible()) < 3):
        player.setVisible(dck.pop())
        print(dck.len())
        player.setHiddenCard(dck.pop())
        print(dck.len())


print([i.getValue() for i in p0.getHand()])
print([i.getValue() for i in p0.getVisible()])
print([i.getValue() for i in p0.getHidden()])
print([i.getValue() for i in p1.getHand()])
print([i.getValue() for i in p1.getVisible)])
print([i.getValue() for i in p1.getHidden()])
print([i.getValue() for i in p2.getHand()])
print([i.getValue() for i in p2.getVisible()])
print([i.getValue() for i in p2.getHidden()])
print([i.getValue() for i in p3.getHand()])
print([i.getValue() for i in p3.getVisible()])
print([i.getValue() for i in p3.getHidden()])


# set initial turnOwner
ctr.setTurnOwner(p0)

# P0 cant put a card from the visible
visibleCard=p0.getVisible()[0]
ctr.putCardFromTable(p0, visibleCard.getValue())
assert visibleCard in p0.getVisible()
assert ctr.getTurnOwner().getId() == p0.getId()

# p0 cant put a card from the hiddenTable
hiddenCard=p0.getVisible()[0]
ctr.putCardFromHidden(p0, 11)  # 11%10-1=0
assert hiddenCard in p0.getHidden()
assert ctr.getTurnOwner().getId() == p0.getId()
