from gameController import *
from player import *
from card import *
from deck import *

A = 20
J = 11
Q = 12
K = 13
JK = 30


ctr2 = GameController([Player(0), Player(1)], False)
ctr2.initGame()
print(ctr2.getPlayers()[0].getId())
print([i.getValue() for i in ctr2.getPlayers()[0].getHand()])
print([i.getValue() for i in ctr2.getPlayers()[0].getVisible()])
print([i.getValue() for i in ctr2.getPlayers()[0].getHidden()])

print(ctr2.getPlayers()[1].getId())
print([i.getValue() for i in ctr2.getPlayers()[1].getHand()])
print([i.getValue() for i in ctr2.getPlayers()[1].getVisible()])
print([i.getValue() for i in ctr2.getPlayers()[1].getHidden()])
