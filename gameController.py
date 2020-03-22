
from card import *
from player import *


class GameController(object):
    def __init__(self, players, deck, flash):
        self.players = players
        self.deck = deck().sort()
        self.cardStack = []
        self.cardOnTop = Card("name",0,"suit")
        self.turnOwner = Player(0,[],[],[])
        self.order = True #true: right, false: left
        self.flash = flash
        self.counter = 0

    def initGame(self):
        for player in self.players:
            #Add 3 cards per player in each box
            for i in range(0,3):
                player.setHand(self.deck.pop())
                player.setTable(self.deck.pop())
                player.setHiddenCard(self.deck.pop())

    #Cards in the stack
    def setCardOnTop(self,card):
        self.cardOnTop=card

    def getCardOnTop(self):
        return self.cardOnTop

    def burn(self):
        self.cardStack = []
    
    def getTurnOwner(self):
        return self.turnOwner

    def getPlayers(self):
        return self.players

    def addCounter(self,player,card):
        if (card.getValue()==self.getCardOnTop().getValue()):
            self.counter+=1
            if (self.counter==4):
                self.burn()
                self.counter=0
                return True


    def putCardOnStack(self,player,card):
        if (isinstance(card,Card)):
            if(card.isValidWith(self.getCardOnTop())):
                if(self.flash):
                    if (card in player.getHand()):
                        self.turnOwner=player
                        self.setCardOnTop(player.popCardFromHand(card))
                    elif (card in player.getTable() and player.getHandLen()==0):
                        self.setCardOnTop(player.popCardFromTable())
                        self.turnOwner=player
                elif (player.getId()==self.turnOwner.getId()):
                    if (card in player.getHand()):
                        self.setCardOnTop(player.popCardFromHand(card))
                    elif (card in player.getTable() and player.getHandLen()==0):
                        self.setCardOnTop(player.popCardFromTable())
                if (not self.addCounter(player,card)):
                    self.endTurn(player)       
            else:
                #wrong card, take all the stack
                player.setManyCardsToHand(self.cardStack)
                self.cardStack=[]
                self.endTurnEffects(player)  
        else: 
            if (card==0):
                #have no cards
                player.setManyCardsToHand(self.cardStack)
                self.cardStack=[]
                self.endTurnEffects(player)  
            elif (player.getId()==self.turnOwner and player.getHandLen()==0 and player.getTableLen==0):
                if (player.getHiddenCards()[card-1].isValidWith(self.getCardOnTop())):
                    self.setCardOnTop(player.popCardFromHidden(card-1))
                    if (not self.addCounter(player,card)):
                        self.endTurnEffects(player)   
                else:
                    #wrong card, take all
                    player.setHand(player.popCardFromHidden(card-1))
                    player.setManyCardsToHand(self.cardStack)
                    self.cardStack=[]
                    self.endTurnEffects(player)  


    def endTurn(self,player,skip=0):
        if (self.order): 
            self.turnOwner=self.players[(self.players.index(player)+1+skip)%len(self.players)]
            while(self.turnOwner.hasNoCards()):
                self.turnOwner=self.players[(self.players.index(player)+1)%len(self.players)]
        else:
            self.turnOwner=self.players[(self.players.index(player)-1-skip)%len(self.players)] 
            while(self.turnOwner.hasNoCards()):
                self.turnOwner=self.players[(self.players.index(player)-1)%len(self.players)] 

    def endTurnEffects(self,player):
        effect = self.getCardOnTop().returnEffect()
        if (effect == "skip"): self.endTurn(2)
        elif (effect == "burn"): 
            self.burn()
        elif (effect == "changeOrder"): 
            self.order = not self.order
            self.endTurn(player)
        elif (effect == "takeAll"):
            self.cardStack.pop()
            if(self.order):
                auxPlayer=self.players[self.players.index(player)+1/len(self.players)]
                while(auxPlayer.hasNoCards):
                    auxPlayer=self.players[self.players.index(auxPlayer)+1/len(self.players)]
                auxPlayer.setManyCardsToHand(self.cardStack)
            else:
                auxPlayer=self.players[self.players.index(player)-1/len(self.players)]
                while(auxPlayer.hasNoCards):
                    auxPlayer=self.players[self.players.index(auxPlayer)-1/len(self.players)]
                auxPlayer.setManyCardsToHand(self.cardStack)
            self.cardStack=[]
            self.endTurn(player,1)
        else: 
            self.endTurn(player)
