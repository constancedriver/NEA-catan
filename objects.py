import random
class PlayerHand:
    def __init__(self, colour:str, VP:int=0, roadsLeft:int=15, settlementsLeft:int=5, citiesLeft:int=4, resources=[], development=[], knightsPlayed:int=0):
        self.colour = colour
        self.VP = VP
        self.roadsLeft = roadsLeft
        self.citiesLeft = citiesLeft
        self.resources = resources
        self.development = development 
        self.knightsPlayed = knightsPlayed

class Piece:
    def __init__(self, colour:str):
        self.colour = colour

class road (Piece):
    def __init__ (self, colour:str, location):
        super().__init__(self,colour)
        self.location = location
class outpost(Piece):
    def __init__ (self, colour:str, location, type:str='settlement'):
        super().__init__(self,colour)
        self.location = location
        self.type = type 
    def upgrade(self):
        self.type = 'city'

class Tile:
    def __init__ (self, resource:str, resouceNumber:int, nodes, isRobberOn:bool=False):
        self.resource = resource
        self.resouceNumber = resouceNumber
        self.nodes = nodes
        self.isRobberOn = isRobberOn
    def getNodes(self):
        for node in self.nodes:
            return(node)
        
class Harbour:
    def __init__ (self, position, type:str):
        self.position = position 
        self.type = type 

playerhand1 = PlayerHand('green')
playerhand2 = PlayerHand('red')
playerHand3 = PlayerHand('blue')

def get_node_from_tile_num(n):
    a = {1 : [(0,0,0), (0,1,0), (1,1,0), (1,1,1), (0,0,1), (1,0,1)],
     2 : [(0,1,-1), (0,1,0), (1,1,0), (1,2,0), (1,2,-1), (0,2,-1)],
     3 : [(0,2,-2), (0,2,-1), (1,2,-1), (1,3,-1), (1,3,-2), (0,3,-2)],
     4 : [(1,0,1), (1,0,2), (2,0,2), (2,1,2), (2,1,1), (1,1,1)],
     5 : [(1,1,0), (1,1,1,), (2,1,1,), (2,2,1), (2,2,0), (1,2,0)],
     6 : [(1,2,-1), (1,2,0), (2,2,0), (2,3,0), (2,3,-1), (1,3,-1)],
     7 : [(1,3,-2), (1,3,-1), (2,3,-1), (2,4,-1), (2,4,-2), (1,4,-2)],
     8 : [(2,0,2), (2,0,3), (3,0,3), (3,1,3), (3,1,2), (2,1,2)],
     9 : [(2,1,1), (2,1,2), (3,1,2), (3,2,2), (3,2,1), (2,2,1)],
     10: [(2,3,-1), (2,3,0), (3,3,0), (3,4,0), (3,4,-1), (2,4,-1)],
     11: [(2,4,-2), (2,4,-1), (3,4,-1), (3,5,-1), (3,5,-2), (2,5,-2)],
     12: [(3,1,2), (3,1,3), (4,1,3), (4,2,3), (4,2,2), (3,2,2)],
     13: [(3,2,1), (3,2,2), (4,2,2), (4,3,2), (4,3,1), (3,3,1)],
     14: [(3,3,0), (3,3,1), (4,3,1), (4,4,1), (4,4,0), (3,4,0)],
     15: [(3,4,-1), (3,4,0), (4,4,0), (4,5,0), (4,5,-1), (3,5,-1)],
     16: [(4,2,2), (4,2,3), (5,2,3), (5,3,3), (5,3,2), (4,3,2)],
     17: [(4,3,1), (4,3,2), (5,3,2), (5,4,2), (5,4,1), (4,4,1)],
     18: [(4,4,0), (4,4,1), (5,4,1), (5,5,1), (5,5,0), (4,5,0)]
    }
    return a[n]
def make_tiles():
    terrains = ['ore', 'ore', 'ore', 'sheep', 'sheep', 'sheep', 'sheep', 'hay', 'hay', 'hay', 'hay', 'wood', 'wood', 'wood', 'wood', 'brick', 'brick', 'brick']
    res_num = [5,6,11,8,3,4,5,9,11,3,8,12,6,4,10,10,2,9]
    random.shuffle(terrains)
    tiles = [Tile(x, res_num[i],get_node_from_tile_num(i)) for i,x in enumerate(terrains)]

def is_adjacent (a:tuple,b:tuple):
    aTotal = sum(a)
    if aTotal % 2 == 0:
        if (a[0]-b[0]==-1 and a[1]-b[1]==0 and a[2]-b[2]==0) or (a[0]-b[0]==0 and a[1]-b[1]==1 and a[2]-b[2]==0) or (a[0]-b[0]==0 and a[1]-b[1]==0 and a[2]-b[2]==1):
            return True 
        else:
            return False
    else: 
        if (a[0]-b[0]==1 and a[1]-b[1]==0 and a[2]-b[2]==0) or (a[0]-b[0]==0 and a[1]-b[1]==-1 and a[2]-b[2]==0) or (a[0]-b[0]==0 and a[1]-b[1]==0 and a[2]-b[2]==-1):
            return True
        else: 
            return False