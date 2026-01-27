import random
import time
import ResourceTilesFile
import PlayerHandFile
import PiecesFile
import GameVisualsFile
import GuiFile

class Game:
    def __init__(self, running:bool=True, tiles:list=None, harbours:list=None, players:list=None,
                roads:list=None, outposts:list=None, longestRoad:int=4, largestArmy:int=2,
                turnIndex:int=0, developmentCards:list=None, state=GameVisualsFile.GameVisuals(),
                askToTrade:list=None, acceptedTrade:list=None):
        self.running = running
        self.tiles = tiles.copy() if tiles is not None else []
        self.harbours = harbours.copy() if harbours is not None else []
        self.players = players.copy() if players is not None else []
        self.roads = roads.copy() if roads is not None else []
        self.outposts = outposts.copy() if outposts is not None else []
        self.longestRoad = longestRoad
        self.largestArmy = largestArmy
        self.turnIndex = turnIndex
        self.developmentCards = developmentCards.copy() if developmentCards is not None else []
        self.state = state
        self.askToTrade = askToTrade.copy() if askToTrade is not None else []
        self.acceptedTrade = acceptedTrade.copy() if acceptedTrade is not None else []

    def make_tiles(self):
        terrains = ['ore', 'ore', 'ore', 'sheep', 'sheep', 'sheep', 'sheep', 'hay', 'hay', 'hay', 'hay', 'wood', 'wood', 'wood', 'wood', 'brick', 'brick', 'brick']
        resNum = [5,6,11,8,3,4,5,9,11,3,8,12,6,4,10,10,2,9]
        random.shuffle(terrains)
        self.tiles = [ResourceTilesFile.Tile(x, resNum[i],ResourceTilesFile.get_node_from_tile_num(i+1)) for i,x in enumerate(terrains)]
        self.tiles.insert(9, ResourceTilesFile.Tile('none', 0, [(2,2,0), (2,2,1), (3,2,1), (3,3,1), (3,3,0), (2,3,0)], True))

    def make_harbours(self):
        types = ['any', 'any','brick', 'brick', 'wood', 'wood', 'any', 'any', 'hay', 'hay', 'ore', 'ore', 'any', 'any', 'sheep', 'sheep', 'any', 'any']
        self.harbours = [PiecesFile.Harbour(x, PiecesFile.get_node_from_harbour_num(i)) for i, x in enumerate(types)]

    def set_development_cards(self):
        for i in range (14):
            self.developmentCards.append(PiecesFile.DevelopmentCards('knight'))
        for i in range (5):
            self.developmentCards.append(PiecesFile.DevelopmentCards('victory point', True))
        for i in range(2):
            self.developmentCards.append(PiecesFile.DevelopmentCards('monopoly'))
            self.developmentCards.append(PiecesFile.DevelopmentCards('year of plenty'))
            self.developmentCards.append(PiecesFile.DevelopmentCards('road building'))
        random.shuffle(self.developmentCards)

    def make_players(self):
        white = PlayerHandFile.PlayerHand('white')
        blue = PlayerHandFile.PlayerHand('blue')
        red = PlayerHandFile.PlayerHand('red')
        orange = PlayerHandFile.PlayerHand('orange')
        self.players.append(white)
        self.players.append(blue)
        self.players.append(red)
        self.players.append(orange)

    def next_turn(self):
        if self.state.rolled or self.state.currentScreen == 'place starting pieces':
            self.game_end()
            self.turnIndex += 1
            if self.turnIndex > 3:
                self.turnIndex = 0 
            for card in self.players[self.turnIndex].development:
                card.able_to_play()
            self.state.rolled = False
            GuiFile.new_turn(self.players[self.turnIndex])

    def previous_turn(self):
        self.turnIndex -= 1
        if self.turnIndex < 0:
            self.turnIndex = 3 
        GuiFile.new_turn(self.players[self.turnIndex])

    def roll_dice(self):
        if self.state.rolled == False or self.state.currentScreen == 'main menu':
            dice1 = random.randint(1,6)
            dice2 = random.randint(1,6)
            GuiFile.display_dice(dice1,dice2)
            self.state.rolled = True
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

    def find_tiles_at_node(self, node:tuple):
        tilesAdjacent = []
        for tile in self.tiles:
            if node in tile.nodes:
                tilesAdjacent.append(tile)
        return tilesAdjacent

    def find_players_on_tile(self,tile):
        playersOnTile = []
        for outpost in self.outposts:
            if outpost.location in tile.nodes and outpost.colour not in playersOnTile:
                playersOnTile.append(outpost.colour)
        return playersOnTile
    
    def adjacent_to_settlement(self,node:tuple):
        adjacentToSettlement = False
        #makes sure at least 2 edges (one node) away from another settlement
        for outpost in self.outposts:
            if self.is_adjacent(node, outpost.location):
                adjacentToSettlement = True
        return adjacentToSettlement
    
    def node_empty(self,node:tuple):
        nodeEmpty = True
        for outpost in self.outposts:
            if outpost.location == node:
                nodeEmpty = False
        return nodeEmpty
    
    def edge_empty(self,nodes:list):
        edgeEmpty = True 
        for road in self.roads:
            if road.location == nodes:
                edgeEmpty = False
        return edgeEmpty
    
    def give_starting_resources(self,node:tuple):
        player = self.players[self.turnIndex]
        for tile in self.find_tiles_at_node(node):
            player.resources.append(tile.resource)
        GuiFile.update_banner_resources(self.players)

    def dice_roll_winner(self, players:list):
        rolls = []
        for player in players:
            GuiFile.screen.fill(GuiFile.get_colour(player.colour))
            rolls.append([self.roll_dice(),player])
            GuiFile.pygame.display.update(1149, 850, 251, 143)
            time.sleep(0.1)
        highestRoll=0
        for i in range (0,len(players),1):
            highestRoll = max(rolls[i][0], highestRoll)
        #highestPlayer = [k for k, item in rolls if item[0] == highestRoll]
        highestPlayer = [player for roll, player in rolls if roll == highestRoll]
        if len(highestPlayer) == 1:
            return highestPlayer[0]
        else:
            return self.dice_roll_winner(highestPlayer)

    def game_set_up(self):
        GuiFile.screen.fill((GuiFile.get_colour('none')))
        GuiFile.pygame.display.flip()
        self.turnIndex = self.players.index(self.dice_roll_winner(self.players))
        self.state.currentScreen = 'place starting pieces'
        self.load_starting_screen()

    def start_game(self):
        if self.state.bots + self.state.humans == 4:
            self.make_tiles()
            self.make_harbours()
            self.make_players()
            self.set_development_cards()
            self.game_set_up()

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

    def build(self):
        selectedNodes = []
        for node in self.state.pressedNodes:
            selectedNodes.append(node)
        self.state.pressedNodes.clear()
        if selectedNodes[0] == selectedNodes[1]:
            self.create_outpost(selectedNodes[0])
        elif self.is_adjacent(selectedNodes[0], selectedNodes[1]):
            self.create_road(selectedNodes)
        GuiFile.create_hex_node_buttons()
        GuiFile.new_turn(self.players[self.turnIndex])
        GuiFile.update_banner_resources(self.players)
        
    def create_settlement(self,node:tuple):
        #settlemets must be attached to a road of the player
        #settlements must be at least 2 edges away from another i.e. not adjacent 
        #settlements cost: 'wood', 'brick', 'sheep', 'hay'
        if (self.state.currentScreen == 'place starting pieces' or self.players[self.turnIndex].connected_to_road(node)) and not(self.adjacent_to_settlement(node)) and self.players[self.turnIndex].sufficient_resources(['wood', 'brick', 'sheep', 'hay']):
            self.outposts.append(self.players[self.turnIndex].build_settlement(node))
            GuiFile.update_vp(self.players[self.turnIndex], self.turnIndex)
            # for their second starting settlement, players get starting resources
            if self.state.currentScreen == 'place starting pieces' and 4 < len(self.outposts) <= 8:
                self.give_starting_resources(node)
           

    def create_city(self,node:tuple):
        #cities are upgraded settlements 
        #cities cost: 'ore', 'ore', 'ore', 'hay', 'hay'
        if self.players[self.turnIndex].settlement_at_node(node) and self.players[self.turnIndex].sufficient_resources(['ore', 'ore', 'ore', 'hay', 'hay']):
            self.players[self.turnIndex].build_city(node)
            GuiFile.update_vp(self.players[self.turnIndex], self.turnIndex)
        
    def create_outpost(self, node:tuple):
        if self.node_empty(node):
            self.create_settlement(node)
        else:
            self.create_city(node)

    def create_road(self,nodes:list):
        if self.edge_empty(nodes) and self.sufficent_resources(self.players[self.turnIndex],['wood', 'brick']):
            if self.state.currentScreen == 'place starting pieces':
                connectedToSettlement = False
                attachedToCorrectSettlement = True
                # check connected to settlement 
                for outpost in self.players[self.turnIndex].outposts:
                    if nodes[0] == outpost.location or nodes[1] == outpost.location:
                        connectedToSettlement = True
                        for road in self.players[self.turnIndex].roads:
                            if road.location[1] == outpost.location or road.location[0] == outpost.location:
                                attachedToCorrectSettlement = False
                                #ensures not building a road attached to the previous settlement built
                if connectedToSettlement and attachedToCorrectSettlement:
                    self.roads.append(self.players[self.turnIndex].build_road(nodes))
                    self.check_longest_road()
                    # when placing starting roads and settlements,
                    #go one round in forwards order each placer placing 1 road and 1 settlement
                    #then go in reverse order so that the last person to play places their second road nd settleemnt directly after their first
                    if len(self.roads) < 4:
                        self.next_turn()
                    elif 4 < len(self.roads) < 8:
                        self.previous_turn()
                    elif len(self.roads) == 8:
                        # end of game set up 
                        self.state.currentScreen = 'game'
                        self.load_game_screen()
            elif self.players[self.turnIndex].connected_to_road(nodes[0]) or self.players[self.turnIndex].connected_to_road(nodes[1]):
                self.roads.append(self.players[self.turnIndex].build_road(nodes))
                self.check_longest_road()

    def steal_longest_road(self):
        #update VP
        for player in self.players:
            if player.hasLongestRoad == True:
                player.hasLongestRoad = False
                player.VP -= 2
        self.players[self.turnIndex].hasLongestRoad = True
        self.players[self.turnIndex].VP += 2
        #update new comparison value 
        self.longestRoad = self.players[self.turnIndex].playerLongestRoad
        #update visuals
        GuiFile.update_vp(self.players[self.turnIndex], self.turnIndex)
        GuiFile.update_longest_road(self.players[self.turnIndex].colour)

    def check_longest_road(self):
        # get all locations to calculate the players longest road
        roads = []
        blocks =[]
        for road in self.players[self.turnIndex].roads:
            roads.append(road.location)
        for player in self.players:
            if player != self.players[self.turnIndex]:
                for outpost in self.players[self.turnIndex].outposts:
                    blocks.append(outpost.location)
        #calculate players longest road and if new longest road update longest road
        self.players[self.turnIndex].playerLongestRoad = self.dfs_max_length(roads, blocks)
        if self.players[self.turnIndex].playerLongestRoad > self.longestRoad:
            self.steal_longest_road()

    def get_road_nodes(self, roads:list):
        nodes = []
        for road in roads:
            nodes.append(road[0])
            nodes.append(road[1])
        return nodes
    
    def find_end_nodes(self, blocked:list, roads:list):
        endNodes = []
        nodes = self.get_road_nodes(roads)
        for node in nodes:
            if nodes.count(node) == 1 and node not in blocked:
                endNodes.append(node)
        return endNodes

    def get_current_adjacent_nodes(self,node:tuple, roads:list):
            adjacentNodes = []
            for road in roads:
                if road[0] == node:
                    adjacentNodes.append(road[1])
                elif road[1] == node:
                    adjacentNodes.append(road[0])
            return adjacentNodes
    
    def create_tree(self, roads:list, blocks:list):
        nodes = self.get_road_nodes(roads)
        tree = {}
        for node in nodes:
            if node in blocks:
                tree.update({node: []})
            else:
                tree.update({node: self.get_current_adjacent_nodes(node, roads)})
        return tree
        
    def dfs_max_length_one_chain(self, tree:dict, node:tuple, visited:list=None, depth:int=0, maxDepth:int=0):
        if not visited:
            visited = []
        visited.append(node) # mark node as visited
        for child in tree[node]:  # recursively visit children
            if child not in visited:
                childDepth = self.dfs_max_length_one_chain(tree,child,visited.copy(), depth+1, max(maxDepth,depth+1))
                # visited is a copy so that is doesnt change every instance of visited and effect the loop
                maxDepth=max(maxDepth, childDepth)
        return maxDepth

    def dfs_max_length(self, roads:list, blocked:list):
        tree = self.create_tree(roads, blocked)
        longestPlayerRoad = 0
        endNodes = self.find_end_nodes(blocked,roads)
        for node in endNodes:
            longestPlayerRoad = max(longestPlayerRoad, self.dfs_max_length_one_chain(tree, node))
        return longestPlayerRoad
    
    def create_development_card(self):
        # developmet cards give you a random card from the pile 
        # cost: 'sheep', 'ore', 'hay'
        if self.sufficent_resources(self.players[self.turnIndex], ['sheep', 'ore', 'hay']):
            self.players[self.turnIndex].buy_development_card(self.developmentCards.pop(0))

    def sufficent_resources(self,player:object,resourcesNeeded:list):
        sufficent = True
        resources = ['wood', 'brick', 'sheep', 'hay', 'ore']
        for resource in resources:
            if player.resources.count(resource) < resourcesNeeded.count(resource):
                sufficent = False
        return sufficent

    def discard_cards(self, chosenCards:list):
        player = self.robber_turn()
        # must discard no. resources DIV 2
        if len(chosenCards) == (len(player.resources)//2) and self.sufficent_resources(player, chosenCards):
            for resource in chosenCards:
                player.resources.remove(resource)
        self.state.discardCards = []
        self.robber_turn()

    def robber_turn(self):
        needToDiscard = []
        for player in self.players:
            #must discard cards if have 7 or more cards
            if len(player.resources) > 6:
                needToDiscard.append(player)
        if len(needToDiscard) == 0:
            GuiFile.select_robber_placement_screen()
            self.state.currentScreen = 'robber'
        else:
            self.state.currentScreen = 'discard'
            GuiFile.discard_cards_screen(player)
            return needToDiscard[0]

    def move_robber(self, tileNum:int):
        tile = self.tiles[tileNum]
        if tile.robberIsOn() == False:
            #the robber cannot be placed on the same tile it was just on
            for resourceTile in self.tiles:
                if resourceTile.robberIsOn == True:
                    resourceTile.robberIsOn = False
            tile.robberIsOn = True
            GuiFile.move_robber(tileNum)
            self.choose_player_to_steal_from()

    def players_on_robber_tile(self):
        playersOnRobberTile = []
        for tile in self.tiles:
            if tile.robberIsOn == True:
                playersOnRobberTile.append(self.find_players_on_tile(tile))
        return playersOnRobberTile
    
    def choose_player_to_steal_from(self):
        self.state.currentScreen = 'robber'
        GuiFile.select_player_to_steal_resource_from(self.players_on_robber_tile())

    def steal_card(self, chosenPlayerNum:int):
        possiblePlayers = self.players_on_robber_tile()
        chosenPlayer = possiblePlayers[chosenPlayerNum]
        self.players[self.turnIndex].resources.append(chosenPlayer.resources.pop(random.randint(0,len(chosenPlayer.resources))))
        self.state.currentScreen = 'game'
        self.load_game_screen()

    def steal_largest_army(self):
        for player in self.players:
            if player.hasLargestArmy == True:
                player.hasLargestArmy = False
                player.VP -= 2
        self.players[self.turnIndex].hasLargestArmy = True
        self.players[self.turnIndex].VP += 2
        self.largestArmy = self.players[self.turnIndex].knightsPlayed
        GuiFile.update_vp(self.players[self.turnIndex], self.turnIndex)
        GuiFile.update_largest_army(self.players[self.turnIndex].colour)
    
    def check_able_to_use(self, typeWanted:str):
        ableToUse = False
        if typeWanted in self.players[self.turnIndex].development:
            for card in self.players[self.turnIndex].development:
                if card.type == typeWanted and card.canPlay:
                    ableToUse = True
        return ableToUse
    
    def play_knight(self):
        if self.check_able_to_use('knight'):
            self.players[self.turnIndex].use_knight()
            if self.players[self.turnIndex].knightsPlayed > self.largestArmy:
                self.steal_largest_army()
            self.load_board()
            GuiFile.select_robber_placement_screen()
            self.draw_robber()
            self.state.currentScreen = 'robber'
    
    def play_monopoly(self,resourceType:str):
        if self.check_able_to_use('monopoly'):
            resourceTypeCount = 0
            for player in self.players:
                resourceTypeCount += player.resources.count(resourceType)
                # removes all instances of the resourceType from the resources list
                player.resources = list(filter(lambda a: a != resourceType, player.resources))
            for i in range(0,resourceTypeCount,1):
                self.players[self.turnIndex].resources.append(resourceType)
            self.players[self.turnIndex].developments.remove('monopoly')
            self.load_game_screen()
        
    def play_year_of_plenty(self):
        if self.check_able_to_use('year of plenty') and len(self.state.yoPlenty) == 2:
            resources = self.state.yoPlenty
            self.players[self.turnIndex].resources.append(resources[0])
            self.players[self.turnIndex].resources.append(resources[1])
            self.players[self.turnIndex].developments.remove('year of plenty')
            self.load_game_screen()

    def play_road_building(self):
        if self.check_able_to_use('road building'):
            for i in range(2):
                self.players[self.turnIndex].resources.append('brick')
                self.players[self.turnIndex].resources.append('wood')
            self.players[self.turnIndex].developments.remove('road building')
            self.load_game_screen()

    def trade_with_bank(self,resourceInput, resourceOutput):
        possibleResources = self.trade_with_harbour()
        #having an outpost on a harbour reduces the number of required resources
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
            self.state.tradeOfferTurn.clear()
            self.state.tradeOfferOthers.clear()
            self.load_game_screen()
    
    def trade_with_harbour(self):
        possibleResources = []
        # in order to get the benifit of a harbour, you must have an outpost on it
        for outpost in self.players[self.turnIndex].outposts:
            for harbour in self.harbours:
                if harbour.position == outpost.location:
                    possibleResources.append(harbour.type)
        return possibleResources

    def complete_trade(self):
        #give resources from player whos turn it is to other player
        for resourceTurn in self.state.tradeOfferTurn:
            self.players[self.turnIndex].resources.remove(resourceTurn)
            self.acceptedTrade[0].resources.append(resourceTurn)
        #give resources from other player to players whos turn it is
        for resourceOther in self.state.tradeOfferOthers:
            self.acceptedTrade[0].resources.remove(resourceOther)
            self.players[self.turnIndex].resource.append(resourceOther)
        self.state.tradeOfferOthers.clear()
        self.state.tradeOfferTurn.clear()
        self.acceptedTrade.clear()
        self.load_game_screen()

    def choose_player_to_trade_with(self,index:int):
        chosenPlayer = self.acceptedTrade(index)
        self.acceptedTrade.clear()
        self.acceptedTrade.append(chosenPlayer)
        self.complete_trade()

    def can_trade_with(self):
        canTradeWith = []
        if self.sufficent_resources(self.players[self.turnIndex], self.state.tradeOfferTurn):
            for player in self.players:
                if self.sufficent_resources(player, self.state.tradeOfferOthers) and player != self.players[self.turnIndex]:
                    canTradeWith.append(player)
        self.askToTrade = canTradeWith
        self.trade_with_players()

    def answered_trade(self,accepted:bool):
        if accepted:
            self.acceptedTrade.append(self.askToTrade.pop(0))
        else:
            del self.askToTrade[0]
        self.trade_with_players()
        
    def trade_with_players(self):
        if len(self.askToTrade) != 0:
            GuiFile.ask_others_for_trade(self.askToTrade[0].colour)
        elif len(self.acceptedTrade) == 1:
            self.complete_trade()
        elif len(self.acceptedTrade) > 1:
            self.state.currentScreen = 'choose player to trade with'
            GuiFile.select_player_to_trade_with(self.acceptedTrade)

    def won(self):
        hasWon = False
        # can only win on your turn because that is the only time you can gain VP
        player = self.players[self.turnIndex]
        if (player.VP + player.development.count('victory points')) >= 10:
            hasWon = True
        return hasWon

    def game_end(self):
        if self.won():
            GuiFile.game_end_screen(self.players[self.turnIndex].colour)
            self.state.currentScreen = 'end'
    
    def draw_robber(self):
        robberTile = 9
        i = 0
        for tile in self.tiles:
            if tile.robberIsOn:
                robberTile = i
            i +=1
        GuiFile.move_robber(self.tiles[robberTile].getNodes()[0])

    def load_board(self):
        GuiFile.screen.fill((GuiFile.get_colour('water')))
        GuiFile.draw_harbours(self.harbours)
        resourceTypes = []
        for tile in self.tiles:
            resourceTypes.append(tile.resource)
        GuiFile.create_game_screen(resourceTypes)
        for road in self.roads:
            GuiFile.draw_road(road)
        for outpost in self.outposts:
            if outpost.isCity:
                GuiFile.draw_city(outpost)
            else: 
                GuiFile.draw_settlement(outpost)
        self.draw_robber()
        
    def load_game_screen(self):
        self.load_board()
        GuiFile.draw_building_key()
        if self.largestArmy >= 3:
            for player in self.players:
                if player.hasLargestArmy:
                    GuiFile.update_largest_army(player.colour)
        if self.longestRoad >=5: 
            for player in self.players:
                if player.hasLongestRoad:
                    GuiFile.update_longest_road(player.colour)
        GuiFile.draw_player_banners(self.players)
        GuiFile.new_turn(self.players[self.turnIndex])
        GuiFile.display_dice(0,0)
        GuiFile.pygame.display.flip()

    def load_starting_screen(self):
        self.load_board()
        GuiFile.draw_player_banners(self.players)
        GuiFile.starting_screen()
        GuiFile.new_turn(self.players[self.turnIndex])

    def cancel_trade(self):
        self.state.tradeOfferOthers.clear()
        self.state.tradeOfferTurn.clear()
        self.load_board()

    def quit(self):
        self.running = False
        GuiFile.pygame.quit()
        GuiFile.sys.exit()
        
    def carry_out_command(self,command):
        action = {'roll dice'           : lambda:self.give_producing_resources(),
                  'play'                : lambda:self.start_game(),
                  'end turn'            : lambda:self.next_turn(),
                  'load game screen'    : lambda:self.load_game_screen(),
                  'play knight'         : lambda:self.play_knight(),
                  'play road building'  : lambda:self.play_road_building(),
                  'play monopoly'  : lambda:self.play_monopoly(command['RESOURCE']),
                  'buy development'     : lambda:self.create_development_card(),
                  'trade choice'        : lambda:self.answered_trade(command['CHOICE']),
                  'steal from player'   : lambda:self.steal_card(command['INDEX']),
                  'trade with player'   : lambda:self.choose_player_to_trade_with(command['INDEX']),
                  'play year of plenty' : lambda:self.play_year_of_plenty(),
                  'cancel trade'        : lambda:self.cancel_trade(),
                  'trade with bank'     : lambda:self.trade_with_bank(),
                  'quit'                : lambda:self.quit()
                  }
        #returns the function but doesnt complete the function
        return action[command['COMMAND']]

# main game loop
def main_loop(game):
    while game.running:
        command = GuiFile.command(game.state.currentScreen)
        if command != None:
            if command['TYPE'] == 'visual':
                if command['COMMAND'] == 'exit rules' and game.state.currentScreen == 'game':
                    action = game.load_game_screen()
                elif command['COMMAND'] == 'exit rules' and game.state.currentScreen == 'place starting pieces':
                    action = game.load_starting_screen()
                else:
                    #handel in game state
                    action = game.state.get_command(command)
            elif command['TYPE'] == 'prog':
                #handel in game file
                action = game.carry_out_command(command)
            if action is None:
                print('ERROR: couldnt find command')
            else: 
                action()
            if len(game.state.pressedNodes) == 2:
                game.build()
    
    GuiFile.pygame.quit()
    GuiFile.sys.exit()

#calling game 
game =  Game()    
GuiFile.start_menu()
main_loop(game)
