import GuiFile

class Piece:
    def __init__ (self, location:list, colour:str):
        self._location = location
        self._colour = colour

    def getLocation(self):
        return self._location
    
    def getColour(self):
        return self._colour

class Road(Piece):
    def __init__ (self, colour:str, location:list):
        super().__init__(location, colour)
        GuiFile.draw_road(self)

class Outpost(Piece):
    def __init__ (self, colour:str, location:tuple, isCity:bool=False):
        super().__init__(location, colour)
        self._isCity = isCity
        GuiFile.draw_settlement(self)

    def getisCity(self):
        return self._isCity
    
    def upgrade(self):
        self.isCity = True
        GuiFile.draw_city(self)
        
class Harbour:
    def __init__ (self, type:str, position):
        self._position = position
        self._type = type 

    def getType(self):
        return self._type
    
    def getPosition(self):
        return self._position

class DevelopmentCards:
    def __init__(self, type:str, canPlay:bool=False):
        self._type = type
        self._canPlay = canPlay
    
    def getCardType(self):
        return self._type
    
    def getCanPlay(self):
        return self._canPlay
    
    def able_to_play(self):
        self._canPlay = True

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
