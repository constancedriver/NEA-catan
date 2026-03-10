import PiecesFile
import random

class PlayerHand:
    defaultResources = [
                'wood','wood','wood','wood',
                'brick','brick','brick','brick',
                'sheep','sheep',
                'hay','hay'
            ]
    def __init__(self, colour:str, VP:int=0, roadsLeft:int=15, settlementsLeft:int=5,
                 citiesLeft:int=4, resources:list=None, development:list=None, knightsPlayed:int=0,
                 roads:list=None, outposts:list=None, hasLargestArmy:bool=False, hasLongestRoad:bool=False,
                 isBot:bool=False, playerLongestRoad:int=0):
        self.colour = colour
        self.VP = VP
        self.roadsLeft = roadsLeft
        self.settlementsLeft = settlementsLeft
        self.citiesLeft = citiesLeft
        self.knightsPlayed = knightsPlayed
        self.hasLargestArmy = hasLargestArmy
        self.hasLongestRoad = hasLongestRoad
        self.isBot = isBot
        self.playerLongestRoad = playerLongestRoad
        # avoid all players sharing the same lists
        self.resources = resources.copy() if resources is not None else self.defaultResources.copy()
        self.development = development.copy() if development is not None else []
        self.roads = roads.copy() if roads is not None else []
        self.outposts = outposts.copy() if outposts is not None else []

    def sufficient_resources(self,resourcesNeeded):
        sufficient = True
        for resource in resourcesNeeded:
            if self.resources.count(resource) < resourcesNeeded.count(resource):
                sufficient = False
        return sufficient
    
    def connected_to_road(self,node):
        connectedToRoadChain = False
        # makes sure it is connected to one of the players existing roads
        for road in self.roads:
            if (road.getLocation()[0] == node or road.getLocation()[1] == node):
                connectedToRoadChain = True
        return connectedToRoadChain
    
    def settlement_at_node(self,node):
        settlementAtNode = False
        for outpost in self.outposts:
            if outpost.getLocation() == node and outpost.getisCity() == False:
                settlementAtNode = True 
        return settlementAtNode       

#before called in game check location     
    def build_settlement(self,node):
        if self.settlementsLeft > 0:
            self.resources.remove('wood')
            self.resources.remove('hay')
            self.resources.remove('sheep')
            self.resources.remove('brick')
            settlement = PiecesFile.Outpost(self.colour,node)
            self.outposts.append(settlement)
            self.VP += 1
            self.settlementsLeft -=1
            return settlement
     
    def build_city(self,node):
        if self.citiesLeft>0:
            for i in range(1,3):
                self.resources.remove('ore')
            for i in range (1,2):
                self.resources.remove('hay')
            for outpost in self.outposts:
                if outpost.getLocation() == node:
                    outpost.upgrade()
            self.VP += 1
            self.citiesLeft -= 1
            self.settlementsLeft += 1
    
    def build_road(self, nodes):
        if self.roadsLeft > 0:
            self.resources.remove('wood')
            self.resources.remove('brick')
            road = PiecesFile.Road(self.colour,nodes)
            self.roads.append(road) 
            self.roadsLeft -= 1
            return road
     
    def buy_development_card(self, developmentCard):
        self.resources.remove('sheep')
        self.resources.remove('hay')
        self.resources.remove('ore')
        self.development.append(developmentCard)

    def discard_resources(self):
        needToDiscard = self.resources // 2
        while needToDiscard > 0:
            wantToDiscard = input('which resource discard')
            if wantToDiscard in self.resources:
                self.resources.remove()
                needToDiscard -= 1
        
    def use_knight(self):
        self.remove_development('knight')
        self.knightsPlayed +=1

    def updateDevelopmentsAbleToUse(self):
        #after having the card for one turn, the player is able to play it 
        for card in self.development:
            if not card.getCanPlay():
                card.able_to_play()

    def getDevelopments(self):
        developments = []
        for card in self.development:
            if card.getCanPlay():
                developments.append(card.getCardType())
        return developments
    
    def remove_development(self, type:str):
        removed = False
        while not removed:
            for card in self.development:
                if card.getCardType() == type:
                    self.development.remove(card)
                    removed = True

class Bot(PlayerHand):
    def __init__(self, colour:str, ownIndex:int, VP:int=0, roadsLeft:int=15, settlementsLeft:int=5,
                 citiesLeft:int=4, resources:list=None, development:list=None, knightsPlayed:int=0,
                 roads:list=None, outposts:list=None, hasLargestArmy:bool=False, hasLongestRoad:bool=False,
                 isBot:bool=True, playerLongestRoad:int=0, playerFavour:list=None):
        super().__init__(colour, VP, roadsLeft, settlementsLeft, citiesLeft, resources, development,
                         knightsPlayed, roads, outposts, hasLargestArmy, hasLongestRoad,
                         isBot, playerLongestRoad)
        self.playerFavour = [4,4,4]
        self.ownIndex = ownIndex
        # []
        
    def accept_trade(self, playerIndex):
        if playerIndex > self.ownIndex:
            playerIndex -= 1
        chosenNum = random.randint(0, self.playerFavour[playerIndex]*2+2, 1)
        if chosenNum >= 6:
            return {'TYPE': 'prog',
                'COMMAND': 'trade choice',
                'CHOICE': True}
        else: 
            return {'TYPE': 'prog',
                'COMMAND': 'trade choice',
                'CHOICE': False}
    
    def decrease_player_favour(self, playerIndex):
        if playerIndex > self.ownIndex:
            playerIndex -= 1
        if self.playerFavour>