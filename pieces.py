class Road:
    def __init__ (self, colour:str, location):
        self.colour = colour
        self.location = location

class Outpost:
    def __init__ (self, colour:str, location, isCity:bool=False):
        self.colour = colour
        self.location = location
        self.isCity = isCity
    def upgrade(self):
        self.isCity = True
        
class Harbour:
    def __init__ (self, position, type:str):
        self.position = position 
        self.type = type 
def world():
    print('hello')
def get_node_from_harbour_num(n):
    a = {0:(0,0,0),
        1:(0,0,1),
        2: (1,0,2),
        3: (2,0,2),
        4: (3,1,3),
        5: (4,1,3),
        6: (5,2,3),
        7: (5,3,3),
        8: (5,4,2),
        9: (5,4,1),
        10: (4,5,0),
        11:(4,5,-1),
        12:(3,5,-2),
        13:(-2,5,-2),
        14:(1,4,-2),
        15:(1,3,-2), 
        16:(0,2,-1),
        17:(0,1,-1)
        }
    return a[n]

s1 = Outpost('white', (3,4,0))
s2 = Outpost('red', (2,1,1), True)