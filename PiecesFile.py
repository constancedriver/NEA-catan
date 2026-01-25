import GuiFile

class Piece:
    def __init__ (self, location:list, colour:str):
        self.location = location
        self.colour = colour

class Road(Piece):
    def __init__ (self, colour:str, location):
        super().__init__(location, colour)
        GuiFile.draw_road(self)

class Outpost(Piece):
    def __init__ (self, colour:str, location, isCity:bool=False):
        super().__init__(location, colour)
        self.isCity = isCity
        GuiFile.draw_settlement(self)
    def upgrade(self):
        self.isCity = True
        GuiFile.draw_city(self)
        
class Harbour:
    def __init__ (self, type:str, position):
        self.position = position
        self.type = type 

class DevelopmentCards:
    def __init__(self, type:str, canPlay:bool=False):
        self.type = type
        self.canPlay = canPlay
    def able_to_play(self):
        self.canPlay = True

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
        13:(2,5,-2),
        14:(1,4,-2),
        15:(1,3,-2), 
        16:(0,2,-1),
        17:(0,1,-1)
        }
    return a[n]
