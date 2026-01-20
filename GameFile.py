import random
import time
import resourceTiles
import playerHand
import pieces
import gameState
import gui

class Game:
    def __init__(self, tiles:list=[], harbours:list=[], players:list=[], roads:list=[], outposts:list=[], longestRoad:int=4, largestArmy:int=2, turnIndex:int=0, developmentCards=[], state=gameState.GameState(), askToTrade:list=[], acceptedTrade:list=[]):
        self.tiles = tiles
        self.harbours = harbours
        self.players = players
        self.roads = roads
        self.outposts = outposts
        self.longestRoad = longestRoad
        self.largestArmy = largestArmy
        self.turnIndex = turnIndex
        self.developmentCards = developmentCards
        self.state = state
        self.askToTrade = askToTrade
        self.acceptedTrade = acceptedTrade

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
            self.developmentCards.append(pieces.DevelopmentCards('knight'))
        for i in range (5):
            self.developmentCards.append(pieces.DevelopmentCards('victory point', True))
        for i in range(2):
            self.developmentCards.append(pieces.DevelopmentCards('monopoly'))
            self.developmentCards.append(pieces.DevelopmentCards('year of plenty'))
            self.developmentCards.append(pieces.DevelopmentCards('road building'))
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
        self.game_end()
        self.turnIndex += 1
        if self.turnIndex > 3:
            self.turnIndex = 0 
        for card in self.players[self.turnIndex].development:
            card.able_to_play()
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

    def find_tiles_at_node(self, node:tuple):
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
            if road.nodes == nodes:
                edgeEmpty = False
        return edgeEmpty
    
    def give_starting_resources(self,node:tuple):
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
        self.state.currentScreen = 'place starting resources'
        self.load_starting_screen()

    def place_starting_settlement(self,node:tuple):
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
        
    def place_starting_road(self, nodes:list):
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
                self.state.currentScreen = 'game'
                self.load_game_screen()
    
    def start_game(self):
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
            
    def create_settlement(self,node:tuple):
        #settlemets must be attached to a road of the player
        #settlements must be at least 2 edges away from another i.e. not adjacent 
        #settlements cost: 'wood', 'brick', 'sheep', 'hay'
        if self.players[self.turnIndex].connected_to_road(node) and not(self.players[self.turnIndex].adjacent_to_settlement(node)) and self.players[self.turnIndex].sufficient_resources(['wood', 'brick', 'sheep', 'hay']):
            self.outposts.append(self.players[self.turnIndex].build_settlement(node))
            gui.update_vp(self.players[self.turnIndex], self.turnIndex)

    def create_city(self,node:tuple):
        #cities are upgraded settlements 
        #cities cost: 'ore', 'ore', 'ore', 'hay', 'hay'
        if self.players[self.turnIndex].settlement_at_node(node) and self.players[self.turnIndex].sufficient_resources(['ore', 'ore', 'ore', 'hay', 'hay']):
            self.players[self.turnIndex].build_city(node)
            gui.update_vp(self.players[self.turnIndex], self.turnIndex)
        
    def create_outpost(self,node:tuple):
        if self.node_empty(node):
            self.create_settlement(node)
        else:
            self.create_city(node)

    def create_road(self,nodes:list):
        if self.edge_empty(nodes) and self.players[self.turnIndex].sufficent_resources(['wood', 'brick']) and (self.players[self.turnIndex].connected_to_road(nodes[0]) or self.players[self.turnIndex].connected_to_road(nodes[1])):
            self.roads.append(self.players[self.turnIndex].build_road(nodes))
#        self.check_longest_road(self)

    def create_development_card(self):
        # developmet cards give you a random card from the pile 
        # cost: 'sheep', 'ore', 'hay'
        if self.players[self.turnIndex].sufficent_resources(['sheep', 'ore', 'hay']):
            self.players[self.turnIndex].buy_development_card(self.developmentCards.pop(0))

    def sufficent_resources(self,player,resourcesNeeded:list):
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
            gui.select_robber_placement_screen()
            self.state.currentScreen = 'robber'
        else:
            self.state.currentScreen = 'discard'
            gui.discard_cards_screen(player)
            return needToDiscard[0]

    def move_robber(self, tileNum:int):
        tile = self.tiles[tileNum]
        if tile.robberIsOn() == False:
            #the robber cannot be placed on the same tile it was just on
            for resourceTile in self.tiles:
                if resourceTile.robberIsOn == True:
                    resourceTile.robberIsOn = False
            tile.robberIsOn = True
            gui.move_robber(tileNum)
            self.choose_player_to_steal_from()

    def players_on_robber_tile(self):
        playersOnRobberTile = []
        for tile in self.tiles:
            if tile.robberIsOn == True:
                playersOnRobberTile.append(self.find_players_on_tile(tile))
        return playersOnRobberTile
    
    def choose_player_to_steal_from(self):
        self.state.currentScreen = 'robber'
        gui.select_player_to_steal_resource_from(self.players_on_robber_tile())

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
        gui.update_vp(self.players[self.turnIndex], self.turnIndex)
        gui.update_largest_army(self.players[self.turnIndex].colour)
    
    def check_able_to_use(self, typeWanted:str):
        ableToUse = False
        if typeWanted in self.players[self.turnIndex].development:
            for card in self.players[self.turnIndex].development:
                if card.type == typeWanted and card.canPlay:
                    ableToUse = True
        return ableToUse
    
    def play_knight(self,tile):
        if self.check_able_to_use('knight'):
            self.move_robber(tile)
            self.steal_card()
            self.players[self.turnIndex].use_knight()
            if self.players[self.turnIndex].knightsPlayed > self.largestArmy:
                self.steal_largest_army()
            self.load_board()
            gui.select_robber_placement_screen()
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
        
    def play_year_of_plenty(self, resourceType1, resourceType2):
        if self.check_able_to_use('year of plenty'):
            self.players[self.turnIndex].resources.append(resourceType1)
            self.players[self.turnIndex].resources.append(resourceType2)
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
            gui.ask_others_for_trade(self.askToTrade[0].colour)
        elif len(self.acceptedTrade) == 1:
            self.complete_trade()
        elif len(self.acceptedTrade) > 1:
            self.state.currentScreen = 'choose player to trade with'
            gui.select_player_to_trade_with(self.acceptedTrade)

    def won(self):
        hasWon = False
        # can only win on your turn because that is the only time you can gain VP
        player = self.players[self.turnIndex]
        if (player.VP + player.developments.count('victory points')) >= 10:
            hasWon = True
        return hasWon

    def game_end(self):
        if self.won():
            gui.game_end_screen(self.players[self.turnIndex].colour)
            self.state.currentScreen = 'end'
    
    def draw_robber(self):
        robberTile = 9
        i = 0
        for tile in self.tiles:
            if tile.robberIsOn:
                robberTile = i
                i +=1
        gui.move_robber(self.tiles[robberTile].getNodes()[0])

    def load_board(self):
        gui.screen.fill((gui.get_colour('water')))
        gui.draw_harbours(self.harbours)
        resourceTypes = []
        for tile in self.tiles:
            resourceTypes.append(tile.resource)
        gui.create_game_screen(resourceTypes)
        for road in self.roads:
            gui.draw_road(road)
        for outpost in self.outposts:
            if outpost.isCity:
                gui.draw_city(outpost)
            else: 
                gui.draw_settlement(outpost)
        self.draw_robber()
        
    def load_game_screen(self):
        self.load_board()
        gui.draw_building_key()
        if self.largestArmy >= 3:
            for player in self.players:
                if player.hasLargestArmy:
                    gui.update_largest_army(player.colour)
        if self.longestRoad >=5: 
            for player in self.players:
                if player.hasLongestRoad:
                    gui.update_longest_road(player.colour)
        gui.draw_player_banners(self.players)
        gui.new_turn(self.players[self.turnIndex])
        gui.pygame.display.flip()

    def load_starting_screen(self):
        self.load_board()
        gui.starting_screen()

    def convert_command(self,command):
        action = {'roll dice'           : self.give_producing_resources(),
                  'play'                : self.start_game(),
                  'end turn'            : self.next_turn(),
                  'load game screen'    : self.load_game_screen(),
                  'play knight'         : self.play_knight(),
                  'play road building'  : self.play_road_building(),
                  'play monopoly wood'  : self.play_monopoly('wood'),
                  'play monopoly brick' : self.play_monopoly('brick'),
                  'play monopoly sheep' : self.play_monopoly('sheep'),
                  'play monopoly hay'   : self.play_monopoly('hay'),
                  'play monopoly ore'   : self.play_monopoly('ore'),
                  'buy development'     : self.create_development_card(),
                  'accepted'            : self.answered_trade(True),
                  'declined'            : self.answered_trade(False),
                  'steal from player index 0': self.steal_card(0),
                  'steal from player index 1': self.steal_card(1),
                  'steal from player index 2': self.steal_card(2),
                  'steal from player index 3': self.steal_card(3),
                  'trade with player index 0': self.choose_player_to_trade_with(0),
                  'trade with player index 1': self.choose_player_to_trade_with(1),
                  'trade with player index 2': self.choose_player_to_trade_with(2),
                  'trade with player index 3': self.choose_player_to_trade_with(3),
        }
        return action[command]
    
    def carry_out_command(self):
        command = self.state.get_command()
        if type(command) == int:
            self.move_robber(command)
        elif type(command) == str:
            self.carry_out_command(command)
        else: # is a list
            if command[0] == 'year of plenty':
                self.play_year_of_plenty(command[1])
            elif command[0] == 'discard cards':
                self.discard_cards(command[1])
            elif command[0] == 'trade with bank':
                self.trade_with_bank(command[1], command[2])
            elif command[0] == 'complete trade':
                self.can_trade_with(command[1], command[2])
            elif len(command) == 2:
                self.create_road(command)
            else: 
                self.create_outpost(command)