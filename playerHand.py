import pieces
import gui

class PlayerHand:
    def __init__(self, colour:str, VP:int=0, roadsLeft:int=15, settlementsLeft:int=5, citiesLeft:int=4, resources:list=['wood', 'wood', 'wood', 'wood', 'brick', 'brick', 'brick', 'brick', 'sheep', 'sheep', 'hay', 'hay'], development:list=[], knightsPlayed:int=0, roads:list=[], outposts:list=[], hasLargestArmy:bool=False, hasLongestRoad:bool=False, isBot:bool=False):
        self.VP = VP
        self.roadsLeft = roadsLeft
        self.settlementsLeft = settlementsLeft
        self.citiesLeft = citiesLeft
        self.resources = resources
        self.development = development 
        self.knightsPlayed = knightsPlayed
        self.roads = roads
        self.outposts = outposts
        self.hasLargestArmy = hasLargestArmy
        self.hasLongestRoad = hasLongestRoad
        self.isBot = isBot
        self.colour = colour

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
            if (road.nodes[0] == node or road.nodes[1] == node):
                connectedToRoadChain = True
        return connectedToRoadChain
    
    def settlement_at_node(self,node):
        settlementAtNode = False
        for outpost in self.outposts:
            if outpost.location == node and outpost.isCity == False:
                settlementAtNode = True 
        return settlementAtNode       

#before called in game check location     
    def build_settlement(self,node):
        if self.settlementsLeft > 0:
            self.resources.remove('wood')
            self.resources.remove('hay')
            self.resources.remove('sheep')
            self.resources.remove('brick')
            settlement = pieces.Outpost(self,node)
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
            node.upgrade()
            self.VP += 1
            self.citiesLeft -= 1
    
    def build_road(self, nodes):
        if self.roadsLeft > 0:
            self.resources.remove('wood')
            self.resources.remove('brick')
            road = pieces.Road(self,nodes)
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
        self.development.remove('knight')
        self.knightsPlayed +=1
