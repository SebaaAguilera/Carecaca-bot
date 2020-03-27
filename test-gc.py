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

# setHands
h0 = dck.popAListByValues([6, JK, 8])
h1 = dck.popAListByValues([6, 10, J])
h2 = dck.popAListByValues([6, 2, 7])
h3 = dck.popAListByValues([6, 7, A])


# setPlayers
p0 = Player(0)
p0.setManyCardsToHand(h0)
p1 = Player(1)
p1.setManyCardsToHand(h1)
p2 = Player(2)
p2.setManyCardsToHand(h2)
p3 = Player(3)
p3.setManyCardsToHand(h3)

pl = [p0, p1, p2, p3]

# setGameController
ctr = GameController()
for p in pl:
    ctr.setPlayer(p)
ctr.changeDeck(dck)

# set visible and hidden visibleCards
for player in ctr.getPlayers():
    player.setManyCardsToVisible(dck.popAListByLen(3))
    player.setManyCardsToHidden(dck.popAListByLen(3))

# set initial turnOwner
ctr.setTurnOwner(p0)

# P0 cant put a card from the visible
visibleCard = p0.getVisible()[0]
put = ctr.putCardFromVisible(p0, visibleCard.getValue())
assert visibleCard in p0.getVisible()
assert ctr.getTurnOwner().getId() == p0.getId()

# p0 cant put a card from the hiddenTable
hiddenCard = p0.getHidden()[0]
put = ctr.putCardFromHidden(p0, 11)  # 11%10-1=0
assert hiddenCard in p0.getHidden()
assert ctr.getTurnOwner().getId() == p0.getId()


# p0 put a 6
handCard = p0.getHand()[0]
put = ctr.putCardFromHand(p0, 6)
assert handCard not in p0.getHand()
assert p0.getHandLen() == 3
assert ctr.getTurnOwner().getId() == p1.getId()
assert ctr.getCounter() == 1


# p1 put a 6
handCard = p1.getHand()[0]
put = ctr.putCardFromHand(p1, 6)
assert handCard not in p1.getHand()
assert p1.getHandLen() == 3
assert ctr.getTurnOwner().getId() == p2.getId()
assert ctr.getCounter() == 2

# p2 put a 6
handCard = p2.getHand()[0]
put = ctr.putCardFromHand(p2, 6)
assert handCard not in p2.getHand()
assert p2.getHandLen() == 3
assert ctr.getTurnOwner().getId() == p3.getId()
assert ctr.getCounter() == 3

# p3 put a 6 and burns the cards, play again
handCard = p3.getHand()[0]
put = ctr.putCardFromHand(p3, 6)
assert handCard not in p3.getHand()
assert p3.getHandLen() == 3
assert ctr.getTurnOwner().getId() == p3.getId()
assert ctr.getCounter() == 0
assert ctr.getCardOnTop() is None
assert len(ctr.getStack()) == 0


# p3 put a 7
handCard = p3.getHand()[0]
put = ctr.putCardFromHand(p3, 7)
assert handCard not in p3.getHand()
assert p3.getHandLen() == 3
assert ctr.getTurnOwner().getId() == p0.getId()
assert ctr.getCounter() == 1

# i'll assume p0 have no useful cards
ctr.takeAll(p0)
assert handCard in p0.getHand()
assert p0.getHandLen() == 4
assert ctr.getTurnOwner().getId() == p1.getId()
assert ctr.getCounter() == 0
assert ctr.getCardOnTop() is None

# p1 play a 10 burn the card and play again
handCard = p1.getHand()[0]
put = ctr.putCardFromHand(p1, 10)
assert handCard not in p1.getHand()
assert p1.getHandLen() == 3
assert ctr.getTurnOwner().getId() == p1.getId()
assert ctr.getCounter() == 0
assert ctr.getCardOnTop() is None
assert len(ctr.getStack()) == 0

# p1 play J changing the
handCard = p1.getHand()[0]
put = ctr.putCardFromHand(p1, J)
assert handCard not in p1.getHand()
assert p1.getHandLen() == 3
assert ctr.getTurnOwner().getId() == p0.getId()
assert ctr.getCounter() == 1
assert ctr.getOrder() == False

# p0 play plays a joker and p3 now have a J
jota = ctr.getCardOnTop()
handCard = p0.getHand()[0]
put = ctr.putCardFromHand(p0, JK)
assert handCard not in p0.getHand()
assert p0.getHandLen() == 3
assert ctr.getTurnOwner().getId() == p2.getId()  # skips p3
assert ctr.getCounter() == 0
assert ctr.getOrder() == False


print("Finished first part!")


dck = Deck(True)

# setHands
h0 = dck.popAListByValues([10, JK, 8])
h1 = dck.popAListByValues([JK, 10, J])
h2 = dck.popAListByValues([6, 2, 7])
h3 = dck.popAListByValues([6, 7, A])


# setPlayers
p0 = Player(0)
p0.setManyCardsToHand(h0)
p1 = Player(1)
p1.setManyCardsToHand(h1)
p2 = Player(2)
p2.setManyCardsToHand(h2)
p3 = Player(3)
p3.setManyCardsToHand(h3)

pl = [p0, p1, p2, p3]

# setGameController
ctr2 = GameController()
for p in pl:
    ctr.setPlayer(p)
ctr2.changeDeck(dck)

# set visible and hidden visibleCards
for player in ctr2.getPlayers():
    player.setManyCardsToVisible(dck.popAListByLen(3))
    player.setManyCardsToHidden(dck.popAListByLen(3))

# set initial turnOwner
ctr2.setTurnOwner(p0)

# p0 put a 10 with no card on top
putCard = ctr2.putCardFromHand(p0, 10)
assert putCard
putCard = ctr2.putCardFromHand(p0, JK)
assert putCard


print("Finished second part!")
