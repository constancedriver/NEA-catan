from pieces import *
class PlayerHand:
    def __init__(self, VP:int=0, roadsLeft:int=15, settlementsLeft:int=5, citiesLeft:int=4, resources=[], development=[], knightsPlayed:int=0, roads=[], outposts=[]):
        self.VP = VP
        self.roadsLeft = roadsLeft
        self.settlementsLeft = settlementsLeft
        self.citiesLeft = citiesLeft
        self.resources = resources
        self.development = development 
        self.knightsPlayed = knightsPlayed
        self.roads = roads
        self.outposts = outposts

#before called in game check location     
    def build_settlement(self,node):
        if 'wood' in self.resources and 'hay' in self.resources and 'brick' in self.resources and 'sheep' in self.resources and self.settlementsLeft > 0:
            self.resources.remove('wood')
            self.resources.remove('hay')
            self.resources.remove('sheep')
            self.resources.remove('brick')
            self.resouces.append(node = Outpost(self,node))
            self.VP += 1
            self.settlementsLeft -=1
    # tell if insuffienctn resoucres 
    def build_city(self,node):
        if self.resources.count('ore') == 3 and self.resources.count('hay') == 2 and self.citiesLeft>0:
            for i in range(1,3):
                self.resources.remove('ore')
            for i in range (1,2):
                self.resources.remove('hay')
            node.upgrade()
            self.VP += 1
            self.citiesLeft -= 1
    # tell if insuffienctn resoucres 
    def build_road(self, nodes):
        if 'wood' in self.resources and 'brick' in self.resources and self.roadsLeft > 0:
            self.resources.remove('wood')
            self.resources.remove('brick')
            self.roads.append(Road(self,nodes)) 
            self.roadsLeft -= 1
    # tell if insufenctn resoucres 