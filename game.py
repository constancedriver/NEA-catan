import random
from resourceTiles import *
from playerHand import *
import pieces
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
        self.tiles = [Tile(x, resNum[i],get_node_from_tile_num(i+1)) for i,x in enumerate(terrains)]
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
        gui.display_dice(dice1,dice2)
        return (dice1+dice2)

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

    def dice_roll_winner(rolls):
        highestRoll = max(rolls.values())
        highestPlayer = [k for k, v in rolls.items() if v == highestRoll]
        return highestPlayer

    def game_set_up(self,startingPlayer):
        self.turnIndex = self.players.index(startingPlayer)
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
    
    def start_game(self,startingPlayer):
        self.make_tiles()
        self.make_harbours()
        self.make_players()
        self.game_set_up(startingPlayer)
        self.set_development_cards()

    def get_producing_tiles(self):
        diceRoll = self.roll_dice()
        diceTotal = diceRoll[0]
        if diceTotal == 7:
            self.robber_turn()
        tilesProducing =[]
        for tile in self.tiles:
            if tile.resourceNumber == diceTotal:
                tilesProducing.append(tile)
        return (tilesProducing,diceRoll[1],diceRoll[2])

    def give_producing_resources(self):
        tilesProducingAndDice = self.get_producing_tiles()
        tilesProducing = tilesProducingAndDice[0]
        for tile in tilesProducing:
            for node in tile.nodes:
                for outpost in self.outposts:
                    if outpost.location == node:
                        outpost.colour.resources.append(tile.resource)
                        if outpost.isCity:
                            outpost.colour.resources.append(tile.resource)
        return(tilesProducingAndDice[1],tilesProducingAndDice[2])
    
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

    def create_settlement(self,node):
        if self.node_empty(node) and self.players[self.turnIndex].connected_to_road(node) and not(self.players[self.turnIndex].adjacent_to_settlement(node)) and self.players[self.turnIndex].sufficient_resources(['wood', 'brick', 'sheep', 'hay']):
            self.outposts.append(self.players[self.turnIndex].build_settlement(node))

    def create_city(self,node):
        if self.players[self.turnIndex].settlement_at_node(node) and self.players[self.turnIndex].sufficient_resources(['ore', 'ore', 'ore', 'hay', 'hay']):
            self.players[self.turnIndex].build_city(node)
    
    def edge_empty(self,nodes):
        edgeEmpty = True 
        for road in self.roads:
            if road.nodes == nodes:
                edgeEmpty = False
        return edgeEmpty

    def create_road(self,nodes):
        if self.edge_empty(nodes) and self.players[self.turnIndex].sufficent_resources(['wood', 'brick']) and (self.players[self.turnIndex].connected_to_road(nodes[0]) or self.players[self.turnIndex].connected_to_road(nodes[1])):
            self.roads.append(self.players[self.turnIndex].build_road(nodes))
        self.check_longest_road(self)

    def create_development_card(self):
        if self.players[self.turnIndex].sufficent_resources(['sheep', 'ore', 'hay']):
            self.players[self.turnIndex].buy_development_card(self.developmentCards[0])
            self.developmentCards.pop(0)

    def robber_turn(self):
        for player in self.players:
            if len(player.resources) > 6:
                player.discard_resources()
        self.move_robber()
        self.steal_card()
    
    def move_robber(self):
        tile = input('tile')
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

    def check_longest_road(self):
        playerRoads = []
        otherPlayerOutposts = []
        for road in self.players[self.turnIndex].roads:
            playerRoads.append(road.location)
        for i in range (0,4,1):
            if i != self.turnIndex:
                for outpost in self.players[i].outposts:
                    otherPlayerOutposts.append(outpost.location)
        


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

    def complete_trade(self, playerTradeWith, inputResources, outputResources):
        for resource in inputResources:
            self.players[self.turnIndex].remove(resource)
            self.players[playerTradeWith].append(resource)
        for resourse in outputResources:
            self.players[self.turnIndex].append(resource)
            self.players[playerTradeWith].remove(resource)

    def trade_with_bank(self,resourceInput, resourceOutput):
        possibleResources = self.trade_with_harbour()
        if resourceInput in possibleResources:
            numberRequired = 2
        elif 'any' in possibleResources:
            numberRequired = 3
        else: 
            numberRequired = 4
        if self.players[self.turnIndex].resources.count(resourceInput) >= numberRequired:
                for i in range (numberRequired):
                    self.players[self.turnIndex].resources.remove(resourceInput)
                self.players[self.turnIndex].resources.append(resourceOutput)
    
    def trade_with_harbour(self):
        possibleResources = []
        for outpost in self.players[self.turnIndex].outposts:
            for harbour in self.harbours:
                if harbour.position == outpost.location:
                    possibleResources.append(harbour.type)
        return possibleResources
    
    def ask_to_trade(self, outputResources):
        playersWantToTrade = []
        # ask each other player if they want to trade
        for i in range (3):
            self.next_turn()
            haveResources = True
            for card in outputResources:
                if self.players[self.turnIndex].resources.count(card) < outputResources.count(card):
                    haveResources = False
            if haveResources: # if they dont have the resources thenthey cannot complete the trade
                wantToTrade = input(self.players[self.turnIndex], 'do you want to trade y/n?')
            else:
                wantToTrade = 'n'
            if wantToTrade == 'y':
                playersWantToTrade.append(self.turnIndex)
            self.next_turn() # get back to to the player whos turn it actually is 
        return playersWantToTrade
    
    def trade_with_players(self, inputResources, outputResources):
        haveResources = True
        for card in inputResources:
            if self.players[self.turnIndex].resources.count(card) < inputResources.count(card):
                haveResources = False
        if haveResources:
            print('trade offer:', inputResources, 'for', outputResources)
            playersWantToTrade = self.ask_to_trade(outputResources)
            if len(playersWantToTrade) == 0:
                print('trade cancelled')
            elif len(playersWantToTrade) == 1:
                tradeIndex = 0
            else:
                tradeIndex = int(input('who would you like to trade with (input index)?', playersWantToTrade))
            self.complete_trade(playersWantToTrade[tradeIndex], inputResources, outputResources)
        else:
            print('insufficient resources')

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
