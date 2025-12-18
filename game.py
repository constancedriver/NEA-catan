import random
from resourceTiles import *
from playerHand import *
import pieces

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
        res_num = [5,6,11,8,3,4,5,9,11,3,8,12,6,4,10,10,2,9]
        random.shuffle(terrains)
        self.tiles = [Tile(x, res_num[i],get_node_from_tile_num(i+1)) for i,x in enumerate(terrains)]
        self.tiles.insert(9, Tile('desert', 0, [(2,2,0), (2,2,1), (3,2,1), (3,3,1), (3,3,0), (2,3,0)], True))

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
        white = PlayerHand()
        blue = PlayerHand()
        red = PlayerHand()
        orange = PlayerHand()
        self.players.append(white)
        self.players.append(blue)
        self.players.append(red)
        self.players.append(orange)

    def next_turn(self):
        self.turnIndex += 1
        if self.turnIndex > 3:
            self.turnIndex = 0 

    def previous_turn(self):
        self.turnIndex -= 1
        if self.turnIndex < 0:
            self.turnIndex = 3 

    def roll_dice(self):
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        diceTotal = dice1+dice2
        return diceTotal

    def get_adjacent_nodes (node:tuple):
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
            if outpost.location in tile.nodes:
                if outpost.colour not in  playersOnTile:
                    playersOnTile.append(outpost.colour)
        return playersOnTile
    
    def give_starting_resources(self,node):
        player = self.players[self.turnIndex]
        for tile in self.find_tiles_at_node(node):
            player.resources.append(tile.resource)

    def game_set_up_rolls(self):
        dicerolls = []
        for player in self.players:
            dicerolls.append(self.roll_dice)
        largest = 0
        for roll in dicerolls:
            if roll > largest:
                largest = roll
        # check if there is a draw
        while dicerolls.count(largest) > 1:
            #reroll drawing players until only one winner
            winners = []
            for i in range (len(dicerolls)):
                if dicerolls[i] == largest:
                    winners.append(i)
            dicerolls = []
            for item in winners:
                dicerolls.append(self.roll_dice)
            largest = 0
            for roll in dicerolls:
                if roll > largest:
                    largest = roll
        # winner starts the game
        self.turnIndex = self.players[dicerolls.index(largest)]

    def game_set_up(self):
        self.game_set_up_rolls()
        for i in range (len(self.players)):
            node1 = input('node')
            self.create_settlement(node1)
            node2 = input('node')
            # road must be attached to settlement 
            while not (self.is_adjacent(node1, node2)):
                node2 = input('enter another node')
            self.create_road((node1,node2))
            self.next_turn()
        for i in range (len(self.players)):
            # for second round goes backwards
            self.previous_turn()
            node1 = input('node')
            self.create_settlement(node1)
            node2 = input('node')
            # road must be attached to settlement 
            while not (self.is_adjacent(node1, node2)):
                node2 = input('enter another node')
            self.create_road((node1,node2))
            #give starting resources 
            self.give_starting_resources(node1)
    
    def start_game(self):
        self.make_tiles()
        self.make_harbours()
        self.make_players()
        self.game_set_up()
        self.set_development_cards()

    def get_producing_tiles(self):
        diceTotal = self.roll_dice()
        if diceTotal == 7:
            self.robber_turn()
        tilesProducing =[]
        for tile in self.tiles:
            if tile.resourceNumber == diceTotal:
                tilesProducing.append(tile)
        return tilesProducing

    def give_producing_resources(self):
        tilesProducing = self.get_producing_tiles()
        for tile in tilesProducing:
            for node in tile.nodes:
                for outpost in self.outposts:
                    if outpost.location == node:
                        outpost.colour.resources.append(tile.resource)
                        if outpost.isCity:
                            outpost.colour.resources.append(tile.resource)

    def create_settlement(self,node):
        player = self.players[self.turnIndex]
        nodeEmpty = True
        connectedToRoadChain = False
        adjacentToSettlement = False
        for outpost in self.outposts:
            if outpost.location == node:
                nodeEmpty = False
        for road in self.roads:
            if (road.nodes[0] == node or road.nodes[1] == node) and road in player.roads:
                connectedToRoadChain = True
        #makes sure at least 2 edges (one node) away from another settlement
        for outpost in self.outposts:
            if self.is_adjacent(node, outpost.location):
                adjacentToSettlement = True
        if nodeEmpty and connectedToRoadChain and not(adjacentToSettlement):
            self.outposts.append(player.build_settlement(node))
    # say that already a settlement at this location

    def create_city(self,node):
        player = self.players[self.turnIndex]
        correctSettlementAtNode = False
        for outpost in self.outposts:
            if outpost.location == node and outpost in player.outposts and outpost.isCity == False:
                correctSettlementAtNode = True
        if correctSettlementAtNode:
            player.build_city(node)
    #say that there isnt appropriate settlemnt at node

    def create_road(self,nodes):
        player = self.players[self.turnIndex]
        edgeEmpty = True 
        connectedToRoadChain = False
        for road in self.roads:
            if road.nodes == nodes:
                edgeEmpty = False
        if edgeEmpty and 'brick' in player.resourses and 'wood' in player.resourses:
            for road in self.roads:
                if (nodes[0] == road.nodes[0] or nodes[0] == road.nodes[1] or nodes[1] == road.nodes[0] or nodes[1] == road.nodes[1]) and road in player.roads:
                    connectedToRoadChain = True
            if connectedToRoadChain:
                self.roads.append(player.build_road(nodes))
                return True
            else:
                return False
        else:
            return False
    
    def create_development_card(self):
        if 'sheep' in self.players[self.turnIndex].resources and 'hay' in self.players[self.turnIndex].resources and 'ore' in self.players[self.turnIndex].resources:
            self.players[self.turnIndex].buy_development_card(self.developmentCards[0])
            self.developmentCards.pop(0)

    def robber_turn(self):
        for player in self.players:
            if len(player.resources) > 6:
                player.discard_resources()
        self.move_robber()
        self.steal_card()
    
    def move_robber(self, tile):
        moved = False
        while not moved:
            if tile.isRobberOn == False:
            #the robber cannot be placed on the same tile it was just on
                for resourceTile in self.tiles:
                    if resourceTile.isRobberOn == True:
                        resourceTile.isRobberOn = False
                tile.isRobberOn = True
                moved = True

    def steal_card(self):
        playersOnRobberTile = []
        for tile in self.tiles:
            if tile.isRobberOn == True:
                playersOnRobberTile = self.find_players_on_tile(tile)
        chosenPlayer = input('choose from:', playersOnRobberTile)
        randomResource = chosenPlayer.resources[random.randint(0,len(chosenPlayer.resources))]
        chosenPlayer.resources.remove(randomResource)
        self.players[self.turnIndex].resources.append(randomResource)

    def steal_largest_army(self):
        for player in self.players:
            if player.hasLargestArmy == True:
                player.hasLargestArmy = False
                player.VP -= 2
        self.players[self.turnIndex].hasLargestArmy = True
        self.players[self.turnIndex].VP += 2
        self.largestArmy = self.players[self.turnIndex].knightsPlayed

    def steal_longest_road(self):
        for player in self.players:
            if player.hasLongestRoad == True:
                player.hasLongestRoad = False
                player.VP -= 2
        self.players[self.turnIndex].hasLongestRoad = True
        self.players[self.turnIndex].VP += 2
#        self.longestRoad = self.players[self.turnIndex] #idk what to call thir longest road segemnt 

    def play_knight(self,tile):
        if 'knight' in self.players[self.turnIndex].developments:
            self.move_robber(tile)
            self.steal_card()
            self.players[self.turnIndex].use_knight()
            if self.players[self.turnIndex].knightsPlayed > self.largestArmy:
                self.steal_largest_army()
    
    def play_monopoly(self,resourceType:str):
        if 'monopoly' in self.players[self.turnIndex].developments:
            resourceTypeCount = 0
            for player in self.players:
                resourceTypeCount += player.resources.count(resourceType)
                # removes all instances of the resourceType from the resources list
                player.resources = list(filter(lambda a: a != resourceType, player.resources))
            for i in range(resourceTypeCount):
                self.players[self.turnIndex].resources.append(resourceType)
            self.players[self.turnIndex].developments.remove('monopoly')

    def play_year_of_plenty(self, resourceType1, resourceType2):
        if 'year of plenty' in self.players[self.turnIndex].developments:
            self.players[self.turnIndex].resources.append(resourceType1)
            self.players[self.turnIndex].resources.append(resourceType2)
            self.players[self.turnIndex].developments.remove('year of plenty')

    def play_road_building(self):
        if 'road building' in self.players[self.turnIndex].developments:
            for i in range(2):
                self.players[self.turnIndex].resources.append('brick')
                self.players[self.turnIndex].resources.append('wood')
            while not self.create_road((make_list , make_list)):
                print('incorrect location')
            while not  self.create_road((make_list, make_list)):
                print('incorrect location') 
            self.players[self.turnIndex].developments.remove('road building')



    def won(self):
        hasWon = False
        for player in self.players:
            if (player.VP + player.developments.count('victory points')) >= 10:
                hasWon = True
        return hasWon
    
    def game_end(self):
        winningVP = 9
        winningPlayer = ''
        for player in self.players:
            if (player.VP + player.developments.count('victory points')) >= winningVP:
                winningVP = (player.VP + player.developments.count('victory points'))
                winningPlayer = player
        return (winningPlayer, 'won with', winningVP, 'points')

def make_list():
    newList = []
    input = ('int')
    while input != '':
        newList.append(int(input))
        input = ('int')
    return newList
