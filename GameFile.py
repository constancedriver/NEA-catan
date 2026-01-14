import random
import time
import resourceTiles
import playerHand
import pieces
import gameState
import gui

class Game:
    def __init__(self, tiles:list=[], harbours:list=[], players:list=[], roads:list=[], outposts:list=[], longestRoad:int=4, largestArmy:int=2, turnIndex:int=0, developmentCards=[]):
        self.tiles = tiles
        self.harbours = harbours
        self.players = players
        self.roads = roads
        self.outposts = outposts
        self.longestRoad = longestRoad
        self.largestArmy = largestArmy
        self.turnIndex = turnIndex
        self.developmentCards = developmentCards

    def make_tiles(self):
        terrains = ['ore', 'ore', 'ore', 'sheep', 'sheep', 'sheep', 'sheep', 'hay', 'hay', 'hay', 'hay', 'wood', 'wood', 'wood', 'wood', 'brick', 'brick', 'brick']
        resNum = [5,6,11,8,3,4,5,9,11,3,8,12,6,4,10,10,2,9]
        random.shuffle(terrains)
        self.tiles = [resourceTiles.Tile(x, resNum[i],resourceTiles.get_node_from_tile_num(i+1)) for i,x in enumerate(terrains)]
        self.tiles.insert(9, resourceTiles.Tile('desert', 0, [(2,2,0), (2,2,1), (3,2,1), (3,3,1), (3,3,0), (2,3,0)], True))

    def make_harbours(self):
        types = ['any', 'any','brick', 'brick', 'wood', 'wood', 'any', 'any', 'hay', 'hay', 'ore', 'ore', 'any', 'any', 'sheep', 'sheep', 'any', 'any']
        self.harbours = [pieces.Harbour(x, pieces.get_node_from_harbour_num(i)) for i, x in enumerate(types)]

    def set_development_cards(self):
        for i in range (14):
            self.developmentCards.append('knight')
        for i in range (5):
            self.developmentCards.append('victory point')
        for i in range(2):
            self.developmentCards.append('monopoly')
            self.developmentCards.append('year of plenty')
            self.developmentCards.append('road building')
        random.shuffle(self.developmentCards)

    def make_players(self):
        white = playerHand.PlayerHand('white')
        blue = playerHand.PlayerHand('blue')
        red = playerHand.PlayerHand('red')
        orange = playerHand.PlayerHand('orange')
        self.players.append(white)
        self.players.append(blue)
        self.players.append(red)
        self.players.append(orange)

    def next_turn(self):
        self.turnIndex += 1
        if self.turnIndex > 3:
            self.turnIndex = 0 
        gui.new_turn(self.players[self.turnIndex])

    def previous_turn(self):
        self.turnIndex -= 1
        if self.turnIndex < 0:
            self.turnIndex = 3 
        gui.new_turn(self.players[self.turnIndex])

    def roll_dice(self):
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        gui.display_dice(dice1,dice2)
        return (dice1+dice2)
    
    def get_adjacent_nodes (self, node:tuple):
        total = sum(node)
        if total % 2 == 0:
            adjacent = [(node[0], node[1], (node[2]+1)), (node[0], (node[1]+1), node[2]), ((node[0]-1), node[1], node[2])]
        else:
            adjacent = [((node[0]+1), node[1], node[2]), (node[0], (node[1]-1), node[2]), (node[0], node[1], (node[2]-1))]
        return adjacent 
    
    def is_adjacent (self,a:tuple,b:tuple):
        if b in self.get_adjacent_nodes(a):
            return True
        else:
            return False

    def find_tiles_at_node(self, node):
        tilesAdjacent = []
        for tile in self.tiles:
            if node in tile.nodes:
                tilesAdjacent.append(tile)

    def find_players_on_tile(self,tile):
        playersOnTile = []
        for outpost in self.outposts:
            if outpost.location in tile.nodes and outpost.colour not in playersOnTile:
                playersOnTile.append(outpost.colour)
        return playersOnTile
    
    def adjacent_to_settlement(self,node):
        adjacentToSettlement = False
        #makes sure at least 2 edges (one node) away from another settlement
        for outpost in self.outposts:
            if self.is_adjacent(node, outpost.location):
                adjacentToSettlement = True
        return adjacentToSettlement
    
    def node_empty(self,node):
        nodeEmpty = True
        for outpost in self.outposts:
            if outpost.location == node:
                nodeEmpty = False
        return nodeEmpty
    
    def give_starting_resources(self,node):
        player = self.players[self.turnIndex]
        for tile in self.find_tiles_at_node(node):
            player.resources.append(tile.resource)
        gui.update_banner_resources([self.players[0].resources, self.players[1].resources, self.players[2].resources, self.players[3].resources])

    def dice_roll_winner(self, players:list):
        rolls = []
        for player in players:
            gui.screen.fill(gui.get_colour(player.colour))
            rolls.append((self.roll_dice()))
            time.sleep(4)
        highestRoll = max(rolls.values())
        highestPlayer = [k for k, v in rolls.items() if v == highestRoll]
        if len(highestPlayer) == 1:
            return highestPlayer[0]
        else:
            self.dice_roll_winner(highestPlayer)

    def game_set_up(self):
        self.turnIndex = self.players.index(self.dice_roll_winner(self.players))
        gameState.state.currentScreen = 'place starting resources'
        self.load_starting_screen()

    def place_starting_settlement(self,node):
        legal = False
        if len(self.outposts) == len(self.roads): # for game set up outposts must be played before roads
            legal = True
            for outpost in self.outposts:
                if self.is_adjacent(outpost.location, node):
                    legal = False
        if legal:
            self.outposts.append(self.players[self.turnIndex].build_settlement)
        if 4 < len(self.outposts) <= 8:
            # get starting resources for the second settlement you place
            self.give_starting_resources(node)
        
    def place_starting_road(self, nodes):
        legal = False
        if self.edge_empty(nodes):
            for node in nodes: # road must be attached to settlement 
                for outpost in self.players[self.turnIndex].outposts:
                    if outpost.location == node:
                        legal = True
        if legal:
            self.outposts.append(self.players[self.turnIndex].build_road(nodes))
            # first do a round of placing settlements going forward
            # then do a round of placing going backwards 
            # such that the last preson places their settlements and roads directly after eachother
            # after this the game set up is done
            if len(self.roads) < 4:
                self.next_turn()
            elif len(self.roads) > 5: 
                self.previous_turn()
            elif len(self.roads) >= 8:
                gameState.state.currentScreen = 'game'
                self.load_game_screen()
    
    def start_game(self):
        self.make_tiles()
        self.make_harbours()
        self.make_players()
        self.set_development_cards()
        self.game_set_up()
        state = gameState.GameState()

    def get_producing_tiles(self):
        diceTotal = self.roll_dice()
        if diceTotal == 7:
            self.robber_turn()
        tilesProducing =[]
        # tiles produce resources when the dice add to their number
        for tile in self.tiles:
            if tile.resourceNumber == diceTotal:
                tilesProducing.append(tile)
        return (tilesProducing)
    
    def give_producing_resources(self):
        tilesProducing = self.get_producing_tiles()
        #the players who have an outpost on a producing tile get a resource of the type the tile produces
        for tile in tilesProducing:
            for node in tile.nodes: # go through all nodes to find the outposts on it 
                for outpost in self.outposts:
                    if outpost.location == node:
                        for player in self.players:
                            if player.colour == outpost.colour:
                                player.resources.append(tile.resource)
                                # cities get an extra resource 
                                if outpost.isCity:
                                    player.resources.append(tile.resource)
            
    def create_settlement(self,node):
        #settlemets must be attached to a road of the player
        #settlements must be at least 2 edges away from another i.e. not adjacent 
        #settlements cost: 'wood', 'brick', 'sheep', 'hay'
        if self.players[self.turnIndex].connected_to_road(node) and not(self.players[self.turnIndex].adjacent_to_settlement(node)) and self.players[self.turnIndex].sufficient_resources(['wood', 'brick', 'sheep', 'hay']):
            self.outposts.append(self.players[self.turnIndex].build_settlement(node))

    def create_city(self,node):
        #cities are upgraded settlements 
        #cities cost: 'ore', 'ore', 'ore', 'hay', 'hay'
        if self.players[self.turnIndex].settlement_at_node(node) and self.players[self.turnIndex].sufficient_resources(['ore', 'ore', 'ore', 'hay', 'hay']):
            self.players[self.turnIndex].build_city(node)