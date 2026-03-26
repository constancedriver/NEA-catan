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
                askToTrade:list=None, acceptedTrade:list=None, currentPlayer:object=None):
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
        self.currentPlayer = currentPlayer

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
        NumBots = self.state.bots
        colours = ['white', 'blue', 'red', 'orange']
        for i in range (0,NumBots, 1):
            self.players.append(PlayerHandFile.BotHand(colours.pop(0), i))
        for i in range (NumBots, 4, 1):
            self.players.append(PlayerHandFile.PlayerHand(colours.pop(0)))
        self.currentPlayer = self.players[self.turnIndex]

    def next_turn(self):
        if self.state.rolled or self.state.currentScreen == 'place starting pieces':
            self.game_end()
            self.turnIndex += 1
            if self.turnIndex > 3:
                self.turnIndex = 0 
            self.currentPlayer.updateDevelopmentsAbleToUse()
            self.state.rolled = False
            GuiFile.new_turn(self.currentPlayer)
            self.currentPlayer = self.players[self.turnIndex]

    def previous_turn(self):
        self.turnIndex -= 1
        if self.turnIndex < 0:
            self.turnIndex = 3 
        self.currentPlayer = self.players[self.turnIndex]
        GuiFile.new_turn(self.currentPlayer)

    def roll_dice(self):
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
            if node in tile.getNodes():
                tilesAdjacent.append(tile)
        return tilesAdjacent

    def find_players_on_tile(self,tile:object):
        playersOnTile = []
        for outpost in self.outposts:
            if outpost.getLocation() in tile.getNodes() and outpost.getColour() not in playersOnTile:
                playersOnTile.append(outpost.getColour())
        return playersOnTile
    
    def adjacent_to_settlement(self,node:tuple):
        adjacentToSettlement = False
        #makes sure at least 2 edges (one node) away from another settlement
        for outpost in self.outposts:
            if self.is_adjacent(node, outpost.getLocation()):
                adjacentToSettlement = True
        return adjacentToSettlement
    
    def node_empty(self,node:tuple): # checks if there is an outpost already on the node 
        nodeEmpty = True
        for outpost in self.outposts:
            if outpost.getLocation() == node:
                nodeEmpty = False
        return nodeEmpty
    
    def edge_empty(self,nodes:list): # checks if there is a road already on the edge
        edgeEmpty = True 
        for road in self.roads:
            # nodes could be stores in either order
            if road.getLocation() == nodes or (road.getLocation()[0] == nodes[1] and road.getLocation()[1] == nodes[0]):
                edgeEmpty = False
        return edgeEmpty
    
    def give_starting_resources(self,node:tuple):
        player = self.currentPlayer
        for tile in self.find_tiles_at_node(node):
            player.resources.append(tile.getTileResource())
        GuiFile.update_banner_resources(self.players)

    def dice_roll_winner(self, players:list):
        rolls = []
        for player in players:
            GuiFile.screen.fill(GuiFile.get_colour(player.colour))
            rolls.append([self.roll_dice(),player])
            GuiFile.pygame.display.update(1149, 850, 251, 143)
            time.sleep(0.5)
        highestRoll=0
        for i in range (0,len(players),1):
            highestRoll = max(rolls[i][0], highestRoll)
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
            return []
        else: 
            tilesProducing =[]
            # tiles produce resources when the dice add to their number
            for tile in self.tiles:
                if tile.getTileNum() == diceTotal and not tile.getIsRobberOn():
                        tilesProducing.append(tile)
            return (tilesProducing)
    
    def give_producing_resources(self):
        if self.state.rolled == False:
        #can only roll the dice once per turn
            tilesProducing = self.get_producing_tiles()
            #the players who have an outpost on a producing tile get a resource of the type the tile produces
            for tile in tilesProducing:
                for outpost in self.outposts:
                    if outpost.getLocation() in tile.getNodes():
                        for player in self.players:
                            if player.colour == outpost.getColour():
                                player.resources.append(tile.getTileResource())
                                if outpost.getisCity():
                                    player.resources.append(tile.getTileResource())
            GuiFile.update_banner_resources(self.players)
            GuiFile.new_turn(self.currentPlayer)

    def build(self, selectedNodes:list=None):
        if selectedNodes == None:
            selectedNodes = []
            for node in self.state.pressedNodes:
                selectedNodes.append(node)
            self.state.pressedNodes.clear()
        if selectedNodes[0] == selectedNodes[1]:
            self.create_outpost(selectedNodes[0])
        elif self.is_adjacent(selectedNodes[0], selectedNodes[1]):
            self.create_road(selectedNodes)
        GuiFile.create_hex_node_buttons()
        GuiFile.new_turn(self.currentPlayer)
        GuiFile.update_banner_resources(self.players)
        
    def create_settlement(self,node:tuple):
        #settlemets must be attached to a road of the player
        #settlements must be at least 2 edges away from another i.e. not adjacent 
        #settlements cost: 'wood', 'brick', 'sheep', 'hay'
        if  ((self.state.currentScreen == 'place starting pieces' and len(self.outposts) == len(self.roads))or (self.currentPlayer.connected_to_road(node) and not(self.adjacent_to_settlement(node)))) and self.currentPlayer.settlementsLeft > 0 and self.currentPlayer.sufficient_resources(['wood', 'brick', 'sheep', 'hay']):
            self.outposts.append(self.currentPlayer.build_settlement(node))
            GuiFile.update_vp(self.currentPlayer, self.turnIndex)
            # for their second starting settlement, players get starting resources
            if self.state.currentScreen == 'place starting pieces' and 4 < len(self.outposts) <= 8:
                self.give_starting_resources(node)
           

    def create_city(self,node:tuple):
        #cities are upgraded settlements 
        #cities cost: 'ore', 'ore', 'ore', 'hay', 'hay'
        if self.currentPlayer.settlement_at_node(node) and self.currentPlayer.sufficient_resources(['ore', 'ore', 'ore', 'hay', 'hay']) and self.currentPlayer.citiesLeft>0:
            self.currentPlayer.build_city(node)
            GuiFile.update_vp(self.currentPlayer, self.turnIndex)
        
    def create_outpost(self, node:tuple):
        if self.node_empty(node):
            self.create_settlement(node)
        else:
            self.create_city(node)

    def create_road(self,nodes:list):
        if self.edge_empty(nodes) and self.sufficent_resources(self.currentPlayer,['wood', 'brick']) and self.currentPlayer.roadsLeft >0:
            if self.state.currentScreen == 'place starting pieces':
                connectedToSettlement = False
                attachedToCorrectSettlement = True
                # check connected to settlement 
                for outpost in self.currentPlayer.outposts:
                    if nodes[0] == outpost.getLocation() or nodes[1] == outpost.getLocation():
                        connectedToSettlement = True
                        for road in self.currentPlayer.roads:
                            if road.getLocation()[1] == outpost.getLocation() or road.getLocation()[0] == outpost.getLocation():
                                attachedToCorrectSettlement = False
                                #ensures not building a road attached to the previous settlement built
                if connectedToSettlement and attachedToCorrectSettlement:
                    self.roads.append(self.currentPlayer.build_road(nodes))
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
            elif self.currentPlayer.connected_to_road(nodes[0]) or self.currentPlayer.connected_to_road(nodes[1]):
                self.roads.append(self.currentPlayer.build_road(nodes))
                self.check_longest_road()

    def steal_longest_road(self):
        #update VP
        i = 0
        for player in self.players:
            if player.hasLongestRoad == True:
                player.hasLongestRoad = False
                player.VP -= 2
                GuiFile.update_vp(self.players[i], i)
            i += 1
        self.currentPlayer.hasLongestRoad = True
        self.currentPlayer.VP += 2
        #update new comparison value 
        self.longestRoad = self.currentPlayer.playerLongestRoad
        #update visuals
        GuiFile.update_vp(self.currentPlayer, self.turnIndex)
        GuiFile.update_longest_road(self.currentPlayer.colour)

    def check_longest_road(self):
        # get all locations to calculate the players longest road
        roads = []
        blocks =[]
        for road in self.currentPlayer.roads:
            roads.append(road.getLocation())
        for outpost in self.outposts:
            if outpost.getColour() != self.currentPlayer.colour:
                blocks.append(outpost.getLocation())
        #calculate players longest road and if new longest road update longest road
        self.currentPlayer.playerLongestRoad = self.dfs_max_length(roads, blocks)
        if self.currentPlayer.playerLongestRoad > self.longestRoad:
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
        if self.sufficent_resources(self.currentPlayer, ['sheep', 'ore', 'hay']) and len(self.developmentCards) > 0:
            print(self.developmentCards[0].getCardType())
            self.currentPlayer.buy_development_card(self.developmentCards.pop(0))
            self.load_game_screen()
            print(self.currentPlayer.colour, 'bought develpoment card')

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
        self.state.discardCards.clear()
        self.robber_turn()

    def find_who_needs_to_discard(self):
        needToDiscard = []
        for player in self.players:
            #must discard cards if have 7 or more cards
            if len(player.resources) >=7:
                needToDiscard.append(player)
        return needToDiscard
    
    def robber_turn(self):
        needToDiscard = self.find_who_needs_to_discard()
        if len(needToDiscard) == 0:
            self.load_game_screen()
            GuiFile.select_robber_placement_screen()
            self.draw_robber()
            self.state.currentScreen = 'robber placement'
        else:
            self.state.currentScreen = 'discard'
            GuiFile.discard_cards_screen(needToDiscard[0].colour)
            GuiFile.new_turn(needToDiscard[0])
            return needToDiscard[0]

    def move_knight(self, tileNum:int):
        tile = self.tiles[tileNum]
        if tile.getIsRobberOn() == False:
            #the robber cannot be placed on the same tile it was just on
            for resourceTile in self.tiles:
                if resourceTile.getIsRobberOn() == True:
                    resourceTile.remove_robber()
            tile.add_robber()
            GuiFile.select_robber_placement_screen()
            GuiFile.move_robber(tileNum)
            # find bots affected by robber movement 
            botsAffected = []
            for player in self.players:
                if player.isBot:
                    for node in tile.getNodes():
                        if player in botsAffected:
                                break
                        for outpost in player.outposts:
                            if player in botsAffected:
                                break
                            if outpost.getLocation() == node:
                                botsAffected.append(player)
            # decrease player favorability 
            for bot in botsAffected:
                bot.decrease_player_favour(self.turnIndex)
            self.choose_player_to_steal_from()

    def players_on_robber_tile(self):
        for tile in self.tiles:
            if tile.getIsRobberOn() == True:
                return (self.find_players_on_tile(tile))
    
    def choose_player_to_steal_from(self):
        self.state.currentScreen = 'robber steal'
        numberOfPlayers = (self.players_on_robber_tile())
        if len(numberOfPlayers) != 0:
            GuiFile.select_player_to_steal_resource_from(self.players_on_robber_tile())
        else:
            self.state.currentScreen = 'game'
            self.load_game_screen()

    def steal_card(self, chosenPlayerNum:int):
        possiblePlayers = self.players_on_robber_tile()
        chosenPlayerColour = possiblePlayers[chosenPlayerNum]
        for player in self.players:
            if player.colour == chosenPlayerColour and len(player.resources) != 0:
                stolenResource = player.resources.pop(random.randint(0,len(player.resources)-1))
                self.currentPlayer.resources.append(stolenResource)
                # update bot favorability (if stolen from decrease)
                if player.isBot:
                    player.decrease_player_favour(self.turnIndex)
        self.state.currentScreen = 'game'
        self.load_game_screen()

    def steal_largest_army(self):
        for player in self.players:
            if player.hasLargestArmy == True:
                player.hasLargestArmy = False
                player.VP -= 2
        self.currentPlayer.hasLargestArmy = True
        self.currentPlayer.VP += 2
        self.largestArmy = self.currentPlayer.knightsPlayed
        GuiFile.update_vp(self.currentPlayer, self.turnIndex)
        GuiFile.update_largest_army(self.currentPlayer.colour)
    
    def play_knight(self):
        if 'knight' in self.currentPlayer.getDevelopments():
            self.currentPlayer.use_knight()
            GuiFile.update_knights(self.currentPlayer, self.turnIndex)
            if self.currentPlayer.knightsPlayed > self.largestArmy:
                self.steal_largest_army()
            self.load_board()
            GuiFile.select_robber_placement_screen()
            self.draw_robber()
            self.state.currentScreen = 'robber placement'
    
    def play_monopoly(self,resourceType:str):
        if 'monopoly' in self.currentPlayer.getDevelopments():
            resourceTypeCount = 0
            for player in self.players:
                resourceTypeCount += player.resources.count(resourceType)
                # removes all instances of the resourceType from the resources list
                player.resources = list(filter(lambda a: a != resourceType, player.resources))
            for i in range(0,resourceTypeCount,1):
                self.currentPlayer.resources.append(resourceType)
            self.currentPlayer.remove_development('monopoly')
            self.load_game_screen()
        
    def play_year_of_plenty(self):
        if 'year of plenty' in self.currentPlayer.getDevelopments() and len(self.state.yoPlenty) == 2:
            resources = self.state.yoPlenty
            self.currentPlayer.resources.append(resources[0])
            self.currentPlayer.resources.append(resources[1])
            self.currentPlayer.remove_development('year of plenty')
            self.load_game_screen()

    def play_road_building(self):
        if 'road building' in self.currentPlayer.getDevelopments():
            for i in range(2):
                self.currentPlayer.resources.append('brick')
                self.currentPlayer.resources.append('wood')
            self.currentPlayer.remove_development('road building')
            self.load_game_screen()

    def trade_with_bank(self,resourceInput:list, resourceOutput:list):
        if len(resourceInput) != 0 and len(resourceOutput) != 0 and self.state.all_same_type(resourceOutput) and self.state.all_same_type(resourceInput):
            possibleResources = self.trade_with_harbour()
            inputResource = resourceInput[0]
            #having an outpost on a harbour reduces the number of required resources
            if inputResource in possibleResources:
                numberRequired = 2 
            elif 'any' in possibleResources:
                numberRequired = 3
            else: 
                numberRequired = 4
            playerResources = self.currentPlayer.resources
            if playerResources.count(inputResource) >= numberRequired:
                for i in range (numberRequired):
                    self.currentPlayer.resources.remove(inputResource)
                self.currentPlayer.resources.append(resourceOutput[0])
                self.state.tradeOfferTurn.clear()
                self.state.tradeOfferOthers.clear()
                self.load_game_screen()
    
    def trade_with_harbour(self):
        possibleResources = []
        # in order to get the benifit of a harbour, you must have an outpost on it
        for outpost in self.currentPlayer.outposts:
            for harbour in self.harbours:
                if harbour.getPosition() == outpost.getLocation():
                    possibleResources.append(harbour.getType())
        return possibleResources

    def complete_trade_player(self):
        #give resources from player whos turn it is to other player
        for resourceTurn in self.state.tradeOfferTurn:
            self.currentPlayer.resources.remove(resourceTurn)
            self.acceptedTrade[0].resources.append(resourceTurn)
        #give resources from other player to players whos turn it is
        for resourceOther in self.state.tradeOfferOthers:
            self.acceptedTrade[0].resources.remove(resourceOther)
            self.currentPlayer.resources.append(resourceOther)
        # update bot favorability
        if self.currentPlayer.isBot:
            print(self.players.index(self.acceptedTrade[0]))
            self.currentPlayer.increase_player_favour(self.players.index(self.acceptedTrade[0]))
        self.state.tradeOfferOthers.clear()
        self.state.tradeOfferTurn.clear()
        self.askToTrade.clear()
        self.acceptedTrade.clear()
        self.load_game_screen()

    def choose_player_to_trade_with(self,index:int):
        chosenPlayer = self.acceptedTrade[index]
        self.acceptedTrade.clear()
        self.acceptedTrade.append(chosenPlayer)
        self.complete_trade_player()

    def can_trade_with(self,resourceInput:list, resourceOutput:list):
        if len(resourceInput) != 0 and len(resourceOutput) != 0 and self.sufficent_resources(self.currentPlayer, resourceInput):
            for player in self.players:
                if self.sufficent_resources(player, resourceOutput) and player != self.currentPlayer:
                    self.askToTrade.append(player)
            if len(self.askToTrade) != 0:
                self.state.currentScreen = 'ask player about trade'
                # if is a bot, run function to see if it accepts the trade
                if self.askToTrade[0].isBot:
                    accepted = self.askToTrade[0].accept_trade(self.turnIndex)
                    self.answered_trade(accepted)
                else:
                    #otherise get input from human
                    GuiFile.ask_others_for_trade(self.askToTrade[0].colour)
            else:
                self.load_game_screen()
               
    def answered_trade(self,accepted:bool):
        if accepted:
            self.acceptedTrade.append(self.askToTrade.pop(0))
        else:
            self.askToTrade.pop(0)
        if len(self.askToTrade) == 0:
            self.state.currentScreen = 'trade'
            self.trade_with_players()
        else:
            self.state.currentScreen = 'ask player about trade'
            # if is a bot, run function to see if it accepts the trade
            if self.askToTrade[0].isBot:
                accepted = self.askToTrade[0].accept_trade(self.turnIndex)
                self.answered_trade(accepted)
            else:
                #otherise get input from human
                GuiFile.ask_others_for_trade(self.askToTrade[0].colour)

    def trade_with_players(self):
        if len(self.acceptedTrade) == 1:
            self.complete_trade_player()
        elif len(self.acceptedTrade) > 1:
            self.state.currentScreen = 'choose player to trade with'
            GuiFile.select_player_to_trade_with(self.acceptedTrade)
        else: 
            self.state.tradeOfferOthers.clear()
            self.state.tradeOfferTurn.clear()
            self.state.currentScreen = 'game'
            self.load_game_screen()

    def won(self):
        hasWon = False
        # can only win on your turn because that is the only time you can gain VP
        player = self.currentPlayer
        if (player.VP + player.getDevelopments().count('victory points')) >= 10:
            hasWon = True
        return hasWon

    def game_end(self):
        if len(self.players) > 0:
            if self.won():
                GuiFile.game_end_screen(self.currentPlayer.colour)
                self.state.currentScreen = 'end'
    
    def draw_robber(self):
        i = 0
        for tile in self.tiles:
            if tile.getIsRobberOn():
                GuiFile.move_robber(i)
            i +=1
        

    def load_board(self):
        GuiFile.screen.fill((GuiFile.get_colour('water')))
        GuiFile.draw_harbours(self.harbours)
        resourceTypes = []
        for tile in self.tiles:
            resourceTypes.append((tile.getTileResource()))
        GuiFile.create_game_screen(resourceTypes)
        for road in self.roads:
            GuiFile.draw_road(road)
        for outpost in self.outposts:
            if outpost.getisCity():
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
        GuiFile.new_turn(self.currentPlayer)
        GuiFile.display_dice(0,0)
        GuiFile.pygame.display.flip()
        self.state.currentScreen = 'game'

    def load_starting_screen(self):
        self.load_board()
        GuiFile.draw_player_banners(self.players)
        GuiFile.starting_screen()
        GuiFile.new_turn(self.currentPlayer)

    def cancel_trade(self):
        self.state.tradeOfferOthers.clear()
        self.state.tradeOfferTurn.clear()
        self.load_game_screen()

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
                  'steal from player'   : lambda:self.steal_card(command['INDEX']),
                  'play road building'  : lambda:self.play_road_building(),
                  'play monopoly'       : lambda:self.play_monopoly(command['RESOURCE']),
                  'play year of plenty' : lambda:self.play_year_of_plenty(),
                  'buy development'     : lambda:self.create_development_card(),
                  'trade choice'        : lambda:self.answered_trade(command['CHOICE']),
                  'cancel trade'        : lambda:self.cancel_trade(),
                  'trade with bank'     : lambda:self.trade_with_bank(self.state.tradeOfferTurn, self.state.tradeOfferOthers),
                  'trade with player'   : lambda:self.can_trade_with(self.state.tradeOfferTurn, self.state.tradeOfferOthers),
                  'choose player trade' : lambda:self.choose_player_to_trade_with(command['INDEX']),
                  'discard cards'       : lambda:self.discard_cards(self.state.discardCards),
                  'choose where to play knight' : lambda:self.move_knight(command['HEX NUMBER']),
                  'build'               : lambda:self.build(command['NODES']),
                  'quit'                : lambda:self.quit()
                  }
        #returns the function but doesnt complete the function
        return action[command['COMMAND']]

