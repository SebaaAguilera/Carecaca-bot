from gameController import *


idUwu = 1093
gc = GameController()
dict = {}
dict[idUwu] = gc

print(dict)
print(dict[idUwu])
print(dict.get(idUwu))
print(dict.get(123))
cosa = dict.pop(idUwu, None)
print(cosa
