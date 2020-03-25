A = 20
J = 11
Q = 12
K = 13
JK = 30


class TextDisplay(object):
    def __init__(self, controller):
        self.controller = controller

    def getPlayersDisplay(self):
        numOfPlayers = self.controller.getPlen()
        players = self.controller.getPlayers()
        playerInfo = []
        for i in range(0, numOfPlayers):
            player = players[i]
            playerInfo.append(
                [player.getId(),
                 self.cardsDisplay(player.getHand()),
                 self.cardsDisplay(player.getVisible()),
                 self.cardsDisplay(player.getHidden, False)
                 ]
            )
        return playerInfo

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
                return ":black_jocker:"
        else:
            return ":blue_book:"

    def auxCardOnTop(self, card):
        if card is None:
            return " "
        else:
            return self.cardDisplay(card)

    # return a list with the display from the player 0 to the player len(players)-1
    def outPutTextDisplay(self):
        plInfo = self.getPlayersDisplay()
        turnOwner = self.controller.getTurnOwner().getId()
        dpls_per_player = ""
        for i in range(0, self.controller.getPlen()):
            for j in range(0, self.controller.getPlen()):
                if (i != j):
                    dpls_per_player += "<b>" + plInfo[j][0] + "'s cards </b>" + \
                        plInfo[j][2] + plInfo[j][3] + "\n\n"
            dpls_per_player += "<b> The turn owner is: __" + turnOwner + "__</b>  \n\n"
            dpls_per_player += "<b> Card on Top: </b>" + self.auxCardOnTop(self.controller.getCardOnTop()) + \
                "\n"
            dpls_per_player += "<b> Any cards to draw? " + \
                str(self.controller.haveCards()) + "</b> \n\n"
            dpls_per_player += "<b>YourCards: </b>\n"
            dpls_per_player += plInfo[i][1] + plInfo[i][2] + plInfo[i][3]
        return dpls_per_player
