A = 20
J = 11
Q = 12
K = 13
JK = 30


class TextDisplay(object):
    def __init__(self, controller):
        self.controller = controller

    def cardsDisplay(self, cards, show=True):
        nc = ""
        for i in range(0, len(cards)):
            nc += self.cardDisplay(cards[i], show) + " "
        return nc + "\n"

    def cardDisplay(self, card, show=True):
        if (show):
            value = card.getValue()
            if (value == A):
                return ":regional_indicator_a:"
            elif (value == 2):
                return ":two:"
            elif (value == 3):
                return ":three:"
            elif (value == 4):
                return ":four:"
            elif (value == 5):
                return ":five:"
            elif (value == 6):
                return ":six:"
            elif (value == 7):
                return ":seven:"
            elif (value == 8):
                return ":eight:"
            elif (value == 9):
                return ":nine:"
            elif (value == 10):
                return ":one::zero:"
            elif (value == J):
                return ":regional_indicator_j:"
            elif (value == Q):
                return ":regional_indicator_q:"
            elif (value == K):
                return ":regional_indicator_k:"
            elif (value == JK):
                return ":black_joker:"
        else:
            return ":blue_square:"

    def auxCardOnTop(self, card):
        if card is None:
            return " "
        else:
            return self.cardDisplay(card)

    # return a list with the display from the player 0 to the player len(players)-1
    def outPutTextDisplay(self):
        players = self.controller.getPlayers()
        turnOwner = self.controller.getTurnOwner().getId()
        dpls_per_player = []
        tableStatus = "** The turn owner is: __" + \
            turnOwner + "__** \n\n" \
            + "** Card on Top: **" + self.auxCardOnTop(self.controller.getCardOnTop()) + \
            "\n" \
            + "** Cards in stack: " + \
            str(len(self.controller.cardStack)) + "** \n" + \
            "** Cards left :" + \
            str(self.controller.deck.len()) + "/108 ** \n\n"
        for i in range(0, self.controller.getPlen()):
            dpls_per_player.append("\n")
        for i in range(0, self.controller.getPlen()):
            for j in range(0, self.controller.getPlen()):
                if (i != j and not players[j].hasNoCards()):  # have cards
                    dpls_per_player[i] += "\n **" + players[j].getId() + "'s cards: ** \n" + \
                        self.cardsDisplay(players[j].getVisible()) \
                        + self.cardsDisplay(players[j].getHidden(), False) \
                        + "\n"
            dpls_per_player[i] += tableStatus

            if players[i].hasNoCards():
                dpls_per_player[i] += "You are not a Care'caca"
            else:
                dpls_per_player[i] += "** Your Cards: **\n"
                dpls_per_player[i] += "** Hand Cards: ** \n" + \
                    self.cardsDisplay(players[i].getHand())
                dpls_per_player[i] += "** Table Cards: ** \n" + \
                    self.cardsDisplay(players[i].getVisible()) \
                    + self.cardsDisplay(players[i].getHidden(), False) + "\n\n"
        return dpls_per_player
