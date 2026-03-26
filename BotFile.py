import random
import GuiFile
resourceTypes = ['sheep', 'hay', 'brick', 'wood', 'ore']

class Bot():
    def __init__(self, game:object, NodeToTiles:dict=None, NodeToResourceScore:dict=None, NodeToBuildScore:dict=None, tradesProposedOnTurn:list=None):
        self.game = game 
        self.NodeToTiles = NodeToTiles.copy() if NodeToTiles is not None else {}
        self.NodeToResourceScore = NodeToResourceScore.copy() if NodeToResourceScore is not None else {}
        self.NodeToBuildScore = NodeToBuildScore.copy() if NodeToBuildScore is not None else {}
        self.tradesProposedOnTurn = tradesProposedOnTurn.copy() if tradesProposedOnTurn is not None else [] #[get form trade, give into trade]

    def get_existing_adjacent_nodes(self, node:tuple):
        board = {(5, 3, 2): [(5, 4, 2), (5, 3, 3)],
            (4, 3, 2): [(5, 3, 2), (4, 2, 2), (4, 3, 1)],
            (4, 2, 2): [(4, 2, 3), (3, 2, 2), (4, 3, 2)],
            (4, 2, 3): [(5, 2, 3), (4, 1, 3)],
            (5, 2, 3): [(4, 2, 3), (5, 3, 3)],
            (5, 3, 3): [(5, 2, 3), (5, 3, 2)],
            (5, 4, 1): [(5, 4, 2), (5, 5, 1), (4, 4, 1)],
            (4, 4, 1): [(5, 4, 1), (4, 3, 1), (4, 4, 0)],
            (4, 3, 1): [(4, 4, 1), (3, 3, 1), (4, 3, 2)],
            (5, 4, 2): [(5, 3, 2), (5, 4, 1)],
            (5, 5, 0): [(5, 5, 1), (4, 5, 0)],
            (4, 5, 0): [(5, 5, 0), (4, 5, -1)],
            (4, 4, 0): [(4, 5, 0), (3, 4, 0), (4, 4, 1)],
            (5, 5, 1): [(5, 4, 1), (5, 5, 0)],
            (3, 2, 2): [(4, 2, 2), (3, 1, 2), (3, 2, 1)],
            (3, 1, 2): [(3, 2, 2), (3, 1, 3), (2, 1, 2)],
            (3, 1, 3): [(3, 1, 2), (3, 0, 3), (4, 1, 3)],
            (3, 0, 3): [(3, 1, 3), (2, 0, 3)],
            (3, 3, 1): [(3, 2, 1), (3, 3, 0), (4, 3, 1)],
            (3, 2, 1): [(3, 2, 2), (3, 3, 1), (2, 2, 1)],
            (3, 4, 0): [(3, 3, 0), (3, 4, -1), (4, 4, 0)],
            (3, 3, 0): [(3, 4, 0), (3, 3, 1), (2, 3, 0)],
            (4, 5, -1):[(4, 5, 0), (3, 5, -1)],
            (3, 5, -1):[(4, 5, -1), (3, 4, -1), (3, 5, -2)],
            (3, 4, -1):[(2, 4, -1), (3, 4, 0), (3, 5, -1)],
            (2, 1, 2): [(3, 1, 2), (2, 0, 2), (2, 1, 1)],
            (2, 0, 2): [(2, 1, 2), (1, 0, 2), (2, 0, 3)],
            (2, 0, 3): [(2, 0, 2), (3, 0, 3)],
            (2, 2, 1): [(2, 1, 1), (2, 2, 0), (3, 2, 1)],
            (2, 1, 1): [(2, 2, 1), (1, 1, 1), (2, 1, 2)],
            (2, 3, 0): [(3, 3, 0), (2, 2, 0), (2, 3, -1)],
            (2, 2, 0): [(1, 2, 0), (2, 3, 0), (2, 2, 1)],
            (2, 4, -1):[(2, 3, -1), (2, 4, -2), (3, 4, -1)],
            (2, 3, -1):[(2, 3, 0), (1, 3, -1), (2, 4, -1)],
            (3, 5, -2):[(3, 5, -1), (2, 5, -2)],
            (2, 5, -2):[(3, 5, -2), (2, 4, -2)],
            (2, 4, -2):[(1, 4, -2), (2, 5, -2), (2, 4, -1)],
            (1, 1, 1): [(2, 1, 1), (1, 1, 0), (1, 0, 1)],
            (1, 0, 1): [(1, 1, 1), (1, 0, 2), (0, 0, 1)],
            (1, 0, 2): [(2, 0, 2), (1, 0, 1)],
            (1, 2, 0): [(2, 2, 0), (1, 2, -1), (1, 1, 0)],
            (1, 1, 0): [(1, 1, 1), (1, 2, 0), (0, 1, 0)],
            (1, 3, -1):[(1, 2, -1), (1, 3, -2), (2, 3, -1)],
            (1, 2, -1):[(1, 2, 0), (1, 3, -1), (0, 2, -1)],
            (1, 4, -2):[(2, 4, -2), (1, 3, -2)],
            (1, 3, -2):[(1, 3, -1), (1, 4, -2), (0, 3, -2)],
            (0, 1, 0): [(1, 1, 0), (0, 1, -1), (0, 0, 0)],
            (0, 0, 0): [(0, 0, 1), (0, 1, 0)],
            (0, 0, 1): [(0, 0, 0), (1, 0, 1)],
            (0, 2, -1):[(0, 1, -1), (0, 2, -2), (1, 2, -1)],
            (0, 1, -1):[(0, 1, 0), (0, 2, -1)],
            (0, 3, -2):[(0, 2, -2), (1, 3, -2)],
            (0, 2, -2):[(0, 2, -1), (0, 3, -2)]}
        return board[node]

    def get_resource_resource_score(self, resourceNum:int):
        # the higher the ResourceScore the higher the probability of producing a resource
        ResourceScore = {8:5,
                        6:5,
                        5:4,
                        9:4,
                        4:3,
                        10:3,
                        3:2,
                        11:2,
                        2:1,
                        12:1,
                        0:0}
        return ResourceScore[resourceNum]

    def find_tiles_at_node(self, node:tuple):
        tiles = self.NodeToTiles.get(node, [])
        if len(tiles) == 0:
            for tile in self.game.tiles:
                if node in tile.getNodes():
                    tiles.append(tile)
            self.NodeToTiles.update({node: tiles})
        return tiles

    def find_harbour_at_node(self, node:tuple):
        for harbour in self.game.harbours:
            if node == harbour.getPosition():
                return harbour 
                # there can only ever be one harbour at a node 
                #this means it can immedately return when it finds a harbour at a node without loosing any harbours
        return None # if no harbour is found at the node

    def find_node_resource_score(self, node:tuple):
        ResourceScore = self.NodeToResourceScore.get(node, 0)
        if ResourceScore == 0:
            #find each tile at the node
            for tile in self.find_tiles_at_node(node):
                #find resource number
                resNum = tile.getTileNum()
                ResourceScore += self.get_resource_resource_score(resNum)
            #finding if there is a harbour at the node
            harbour = self.find_harbour_at_node(node)
            if harbour != None:
                #3:1 (any) are worth 2 and all others are worth 1 point
                if harbour.getType() == 'any':
                    ResourceScore += 2
                else:
                    ResourceScore += 1
            self.NodeToResourceScore.update({node: ResourceScore})
        return ResourceScore

    def decide_discard_cards(self):
        resources = self.game.currentPlayer.resources.copy()
        numberToDiscard =  len(self.game.currentPlayer.resources) // 2
        while len(resources) >  numberToDiscard:
            if self.can_build_city() and resources.count('hay') >= 2 and resources.count('ore') >= 3 and len(resources) >=  numberToDiscard+5:
                for i in range (0,2,1):
                    resources.remove('hay')
                    resources.remove('ore')
                resources.remove('ore')
            elif self.can_build_settlement() and 'hay' in resources and 'sheep' in resources and 'wood' in resources and 'brick' in resources and len(resources) >=  numberToDiscard+4:
                resources.remove('hay')
                resources.remove('brick')
                resources.remove('wood')
                resources.remove('sheep')
            elif self.can_build_road() and 'brick' in resources and 'wood' in resources and len(resources) >=  numberToDiscard+2:
                resources.remove('brick')
                resources.remove('wood')
            elif self.can_buy_development() and 'hay' in resources and 'sheep' in resources and 'ore' in resources and len(resources) >=  numberToDiscard+3:
                resources.remove('hay')
                resources.remove('ore')
                resources.remove('sheep')
            else:
                resources.remove(random.choice(resources))
        for resource in resources:
            print(resources)
            self.game.state.discardCards.append(resource)
        return {'TYPE': 'prog',
                'COMMAND': 'discard cards'}

    def decide_player_steal_from(self): 
        leastFavourableResourceScore = 12
        leastFavourablePlayer = []
        currentBot = self.game.currentPlayer
        playerObjectsOnRobber = []
        #covert colours from players_on_robber_tile to the player objects 
        for player in self.game.players_on_robber_tile():
                for playerObject in self.game.players:
                    if player == playerObject.colour:
                        playerObjectsOnRobber.append(playerObject)
        # find lowest favour ResourceScore of players that can steal from
        for player in playerObjectsOnRobber:
            playerIndex = self.game.players.index(player)
            leastFavourableResourceScore = min(currentBot.get_favour_score(playerIndex), leastFavourableResourceScore)
        # print(leastFavourableResourceScore)
        # find which player(s) have this lowest ResourceScore
        for playerObject in playerObjectsOnRobber:
            playerIndex = self.game.players.index(playerObject)
            if currentBot.get_favour_score(playerIndex) == leastFavourableResourceScore:
                leastFavourablePlayer.append(playerObject)
        # if more than one least favoured, pick a random one of them
        chosen = random.choice(leastFavourablePlayer)
        return {'TYPE': 'prog',
                'COMMAND': 'steal from player',
                'INDEX': playerObjectsOnRobber.index(chosen)}

    def decide_move_robber(self):
        tileSettlements = []
        currentTurnColour = self.game.currentPlayer.colour
        for tile in self.game.tiles:
            nodes = tile.getNodes()
            numberOfSettlements = 0
            for outpost in self.game.outposts:
                if outpost.getLocation() in nodes:
                    if outpost.getColour() == currentTurnColour:
                        numberOfSettlements -= 10
                        # ensures wont be chosen if the bot has a settlement on the tile
                    else:
                        if outpost.getisCity():
                            numberOfSettlements += 2 # a city is equivalient to 2 settlemnts becase it doubles the number of resources and VP
                        else:
                            numberOfSettlements += 1
            tileSettlements.append(numberOfSettlements)
        mostSettlements = 0
        for item in tileSettlements:
            mostSettlements = max(item, mostSettlements)
        #if only one tiles has the most settlements pick it
        if tileSettlements.count(mostSettlements) == 1:
            chosenTile = tileSettlements.index(mostSettlements)
        #otherwise choose one with higher ResourceScore (prop of producing resources)
        else:
            bestTileIndexResourceScore = []
            for i in range (0, len(tileSettlements), 1):
                if tileSettlements[i] == mostSettlements:
                    #add to bestTileIndexResourceScore [index of the tile, resource ResourceScore of the tile]
                    bestTileIndexResourceScore.append([i, self.get_resource_resource_score(self.game.tiles[i].getTileNum())])
            highestResourceScore = 0
            for ResourceScore in bestTileIndexResourceScore:
                highestResourceScore = max(highestResourceScore, ResourceScore[1])
            for index in bestTileIndexResourceScore:
                # if it doesnt have the highest ResourceScore remove it from the list of possible ones to be chosen
                if index[1] != highestResourceScore:
                    bestTileIndexResourceScore.remove(index)
            if len(bestTileIndexResourceScore) == 1:
                chosenTile = bestTileIndexResourceScore[0][0]
            #if same ResourceScore choose a random one
            else:
                chosenTile = random.choice(bestTileIndexResourceScore)[0]
        return {'TYPE': 'prog',
                'COMMAND': 'choose where to play knight',
                'HEX NUMBER': chosenTile}


    def can_build_city(self):
        atLeastOneSettlement = False
        for outpost in self.game.currentPlayer.outposts:
            if atLeastOneSettlement:
                break
            if not outpost.getisCity():
                atLeastOneSettlement = True
        return atLeastOneSettlement

    def can_build_settlement(self):
        if len(self.location_to_build_settlement())!= 0 and self.game.currentPlayer.sufficient_resources(['sheep', 'hay', 'brick', 'wood']):
            return True
        else:
            return False
        
    def can_buy_development(self):
        if len(self.game.developmentCards) != 0 and self.game.currentPlayer.sufficient_resources(['sheep', 'hay', 'ore']):
            return True
        else:
            return False
        
    def can_build_road(self):
        if self.game.currentPlayer.sufficient_resources(['wood', 'brick']):
            emptyEdge = False
            roads = self.game.currentPlayer.roads
            # find is there is at least one road who has an empty adjacent edge
            for road in roads:
                if emptyEdge:
                    break
                for location in road.getLocation():
                    if emptyEdge:
                        break
                    for node in self.game.get_adjacent_nodes(location):
                        if self.game.edge_empty([location, node]):
                            emptyEdge = True
                            break 
            return emptyEdge
        return False

    def try_to_build_city(self):
        settlements = []
        for outpost in self.game.currentPlayer.outposts:
            if not outpost.getisCity():
                settlements.append(outpost)
        if len(settlements) != 0:
            ResourceScores = []
            for settlement in settlements:
                ResourceScores.append(self.find_node_resource_score(settlement.getLocation()))
            highestResourceScore=0
            for i in range (0,len(settlements),1):
                highestResourceScore = max(ResourceScores[i], highestResourceScore)
            if ResourceScores.count(highestResourceScore) == 1:
                settlementIndex = ResourceScores.index(highestResourceScore)    
            else:
                # will pick a random settlemnt with the highest ResourceScore
                possibleIndexes = []
                for i in range (0,len(ResourceScores),1):
                    if ResourceScores[i] == highestResourceScore:
                        possibleIndexes.append(i)
                settlementIndex = random.choice(possibleIndexes)
            node = settlements[settlementIndex].getLocation()
            return {'TYPE': 'prog',
                    'COMMAND': 'build',
                    'NODES': [node, node]}

    def location_to_build_settlement(self):
        possibleLocations = []
        for road in self.game.currentPlayer.roads:
            for location in road.getLocation():
                if self.game.node_empty(location) and not self.game.adjacent_to_settlement(location):
                    possibleLocations.append(location)
        return possibleLocations

    def try_to_build_settlement(self):
        highestResourceScore = 0
        possibleLocations = self.location_to_build_settlement()
        bestNodes = []
        # print('possible locations', possibleLocations)
        for location in possibleLocations:
            highestResourceScore = max (highestResourceScore, self.find_node_resource_score(location))
        for node in possibleLocations:
            if self.find_node_resource_score(node) == highestResourceScore:
                bestNodes.append(node)
                # print('adding to best node', node)
        if len(bestNodes) == 1:
            return {'TYPE': 'prog',
                    'COMMAND': 'build',
                    'NODES': [bestNodes[0], bestNodes[0]]} 
        else:  
            randomNode = random.choice(bestNodes)  
            return {'TYPE': 'prog',
                    'COMMAND': 'build',
                    'NODES': [randomNode, randomNode]} 

    def try_to_build_road(self):
        allowsNewSettlement = self.allows_build_settlement()
        if len(allowsNewSettlement) == 1:
            return {'TYPE': 'prog',
                    'COMMAND': 'build',
                    'NODES': [allowsNewSettlement[0][0], allowsNewSettlement[0][1]]} 
        elif len(allowsNewSettlement) > 1:
            access = self.already_have_access()
            newNodes = []
            # find which of the nodes in the road is the new node 
            for road in allowsNewSettlement:
                for location in road:
                    if location not in access:
                        newNodes.append(location)
            # find node(s) with best resource score
            maxResourceScore = 0
            for node in newNodes:
                maxResourceScore = max(maxResourceScore, self.find_node_resource_score(node))
            bestNodes = []
            for node in newNodes:
                if self.find_node_resource_score(node) == maxResourceScore:
                    bestNodes.append(node)
            # choose a road with the best resource score and build it 
            chosenNode = random.choice(bestNodes)
            for road in allowsNewSettlement:
                if chosenNode in road:
                    return {'TYPE': 'prog',
                    'COMMAND': 'build',
                    'NODES': [road[0], road[1]]} 
        else:
            # no roads create access to a new place to build a settlement 
            # choose a random road to build 
            randomRoad = random.choice(self.possible_road_locations())
            return {'TYPE': 'prog',
                    'COMMAND': 'build',
                    'NODES': [randomRoad[0], randomRoad[1]]} 

    def allows_build_settlement(self):
        possibleLocations = self.possible_road_locations()
        access = self.already_have_access()
        allowsNewSettlement = []
        for roadLocation in possibleLocations:
            giveNewSettlement = False
            for node in roadLocation:
                if node not in access and not self.game.adjacent_to_settlement(node):
                    giveNewSettlement = True
            if giveNewSettlement:
                allowsNewSettlement.append(roadLocation)
        return allowsNewSettlement

    def possible_road_locations(self):
        access = self.already_have_access()
        possibleRoadLoactions = []
        for location in access: 
            adjacentNodes = self.get_existing_adjacent_nodes(location)
            for node in adjacentNodes:
                if self.game.edge_empty([location, node]):
                    possibleRoadLoactions.append([location, node])
        return possibleRoadLoactions

    def already_have_access(self):
        access = []
        for road in self.game.currentPlayer.roads:
            for location in road.getLocation():
                if location not in access:
                    access.append(location)
        return access

    def try_to_build_development_card(self):
        if self.can_buy_development():  
            return {'TYPE': 'prog',
                    'COMMAND': 'buy development'}
        
    def trade_with_bank(self, resourceWant:str, resourceGiveAway:str):
        harbours = self.game.trade_with_harbour()
        numberGive = 0
        if resourceGiveAway in harbours:
            numberGive += 2
        elif 'any' in harbours:
            numberGive += 3
        else:
            numberGive += 4
        for i in range (0,numberGive,1):
            self.game.state.tradeOfferTurn.append(resourceGiveAway)
        self.game.state.tradeOfferOthers.append(resourceWant)
        # allows other players to see what the trade being proposed is 
        print(self.game.currentPlayer.colour, 'traded with bank', self.game.state.tradeOfferTurn, 'for', self.game.state.tradeOfferOthers[0])
        return {'TYPE': 'prog',
                'COMMAND': 'trade with bank'}

        
    def try_trade(self):
        mostWantedNumber = 0
        mostWantedResource = []
        couldTrade = []
        infomation = self.what_to_trade()
        dontTrade = infomation[0]
        want = infomation[1]
        if len(want) == 0: # no point in trading 
            self.tradesProposedOnTurn.append('strike')
            self.tradesProposedOnTurn.append('strike')
            #after two strikes the bot will stop proposing trades
        else: 
            playerResources = self.game.currentPlayer.resources
            #decide which resource to trade based on which was wanted the most number of times
            for resource in resourceTypes:
                mostWantedNumber = max(mostWantedNumber, want.count(resource))
            for resource in resourceTypes:
                if want.count(resource) and mostWantedNumber != 0:
                    mostWantedResource.append(resource)
            while len(mostWantedResource) > 1:
                mostWantedResource.remove(random.choice(mostWantedResource))
            #decide which resource to give away in the trade
            harbours = self.game.trade_with_harbour()
            for resource in resourceTypes:
                if playerResources.count(resource)>=dontTrade.count(resource)+4 or ('any' in harbours and playerResources.count(resource)>=dontTrade.count(resource)+3) or (resource in harbours and playerResources.count(resource)>=dontTrade.count(resource)+2):
                    # can trade wiht bank 
                    return self.trade_with_bank(mostWantedResource[0], resource)
                elif playerResources.count(resource)>dontTrade.count(resource):
                    couldTrade.append(resource)
            for item in couldTrade:
                if [mostWantedResource[0], item] in self.tradesProposedOnTurn:
                    #removing trades offers that have already been done 
                    couldTrade.remove(item)
            if len(couldTrade) == 0:
                self.tradesProposedOnTurn.append('strike')#after two strikes the bot will stop proposing trades
            else:
                while len(couldTrade)>1:
                    couldTrade.remove(random.choice(couldTrade))
                #add to list of trades proposed
                self.tradesProposedOnTurn.append([mostWantedResource[0], couldTrade[0]])
                #propose trade
                self.game.state.tradeOfferTurn.append(couldTrade[0])
                self.game.state.tradeOfferOthers.append(mostWantedResource[0])
                GuiFile.trade_screen()
                GuiFile.redraw_trade_offer_you(self.game.state.tradeOfferOthers, True)
                GuiFile.redraw_trade_offer_you(self.game.state.tradeOfferTurn, False)
                GuiFile.pygame.display.flip()   
                return {'TYPE': 'prog',
                    'COMMAND': 'trade with player'}

    def what_to_trade(self):
        resources = self.game.currentPlayer.resources
        dontTrade = []
        want = []
        # if one away from having a city and enough spare to trade for one
        if ((resources.count('hay') == 1 and resources.count('ore') == 3) or  (resources.count('hay') == 2 and resources.count('ore') == 2))and len(resources)>4:
            want.append('hay')
            want.append('ore')
            for i in range (0,resources.count('hay')):
                dontTrade.append('hay')
                # if have enough hay, doesnt want hay
                if i == 1:
                    want.remove('hay')
                    break # only add up to 2 day to dontTrade
            for i in range (0,resources.count('ore')):
                dontTrade.append('ore')
                if i == 2:
                    want.remove('ore')
                    break
        #if one anway from having a settlement and enough spare to trade
        if len(resources) and 'sheep' in resources and 'hay' in resources and 'wood' in resources:
            want.append('brick')
            dontTrade.append('sheep')
            dontTrade.append('wood')
            dontTrade.append('hay')
        elif len(resources) and 'brick' in resources and 'hay' in resources and 'wood' in resources:
            want.append('sheep')
            dontTrade.append('brick')
            dontTrade.append('wood')
            dontTrade.append('hay')
        elif len(resources) and 'sheep' in resources and 'brick' in resources and 'wood' in resources:
            want.append('hay')
            dontTrade.append('sheep')
            dontTrade.append('wood')
            dontTrade.append('brick')
        elif len(resources) and 'sheep' in resources and 'hay' in resources and 'brick' in resources:
            want.append('wood')
            dontTrade.append('sheep')
            dontTrade.append('brick')
            dontTrade.append('hay')
        # or if one away from getting a road and sufficient resources to trade
        # (elif because resources for road is a subclass of resources for settlement)
        elif len(resources) > 1 and 'wood' in resources:
            want.append('brick')
            dontTrade.append('wood')
        elif len(resources) > 1 and 'brick' in resources:
            want.append('wood')
            dontTrade.append('brick')
        #or development card
        elif len(resources) > 2 and 'sheep' in resources and 'hay' in resources:
            want.append('ore')
            dontTrade.append('sheep')
            dontTrade.append('hay')
        # these combinations not a subclass but a development card lowest in prioroty
        elif len(resources) > 2 and 'ore' in resources and 'hay' in resources:
            want.append('sheep')
            dontTrade.append('ore')
            dontTrade.append('hay')
        elif len(resources) > 2 and 'sheep' in resources and 'ore' in resources:
            want.append('hay')
            dontTrade.append('sheep')
            dontTrade.append('ore')
        return [dontTrade, want]

    def calculate_trade_score(self, player:object):
        score = 0
        #add favour score 
        score += self.game.currentPlayer.get_favour_score(self.game.players.index(player))
        #take away number of VP /2
        score -= player.VP
        return score

    def who_to_trade_with(self):
        playersAccepted = self.game.acceptedTrade
        bestScore = self.calculate_trade_score(playersAccepted[0]) #ensures starting score isnt too high
        bestPlayers = []
        # find player(s) with best trade score
        for player in playersAccepted:
            tradeScore = self.calculate_trade_score(player)
            if bestScore < tradeScore:
                bestScore == tradeScore
                bestPlayers.clear()
                bestPlayers.append(player)
            elif bestScore == tradeScore:
                bestPlayers.append(player)
        return {'TYPE': 'prog',
                'COMMAND': 'choose player trade',
                'INDEX' : playersAccepted.index(random.choice(bestPlayers))}

    def get_tiles_at_node(self, node:tuple):
        tilesAtNode = []
        for tile in self.game.tiles:
            if node in tile.getNodes():
                tilesAtNode.append(tile)
        return tilesAtNode

    def get_starting_score(self,node:tuple):
        score = self.find_node_resource_score(node)
        resourcesAtNode = []
        for tile in self.get_tiles_at_node(node):
            resource = tile.getTileResource()
            #dont want duplications of resources 
            if resource not in resourcesAtNode:
                resourcesAtNode.append(resource)
        score += len(resourcesAtNode) # adds extra for more types of resources 
        #prioritise wood and brick 
        if 'wood' in resourcesAtNode:
            score += 2
        if 'brick' in resourcesAtNode:
            score += 2
        return score 

    def starting_pieces(self):
        numberOfRoads = len(self.game.currentPlayer.roads)
        numberofOutposts = len(self.game.currentPlayer.outposts)
        if numberOfRoads == numberofOutposts:
            #place a settlement
            bestScore = -1
            bestNodes = []
            for tile in self.game.tiles:
                for node in tile.getNodes():
                    #if a legal place to play
                    if self.game.node_empty(node) and not self.game.adjacent_to_settlement(node):
                        startingScore = self.get_starting_score(node)
                        if startingScore > bestScore:
                            bestScore = startingScore
                            bestNodes.clear()
                            bestNodes.append(node)
                        elif startingScore == bestScore:
                            bestNodes.append(node)
            randomNode = random.choice(bestNodes)
            return {'TYPE': 'prog',
                'COMMAND': 'build',
                'NODES': [randomNode, randomNode]} 
        else:
            #build a road
            for outpost in self.game.currentPlayer.outposts:
                roadAttached = False
                outpostLocation = outpost.getLocation()
                for road in self.game.currentPlayer.roads:
                    if outpostLocation in road.getLocation():
                        roadAttached = True
                if not roadAttached:
                    settlementToBuildFrom = outpostLocation
                    #beacuse of the way the game set up works, one of the settlements wont have an attached road
            return {'TYPE': 'prog',
                    'COMMAND': 'build',
                    'NODES': [settlementToBuildFrom, random.choice(self.get_existing_adjacent_nodes(settlementToBuildFrom))]} 
            
    def robber_on_player_tile(self):
        if self.game.currentPlayer.colour in self.game.players_on_robber_tile():
            return True
        else:
            return False
        
    def should_play_yop(self):
        if self.can_build_city():
            cityResources = ['hay', 'hay', 'hay', 'ore', 'ore']
            for resource in self.game.currentPlayer.resources:
                if resource in cityResources:
                    cityResources.remove(cityResources) # will remove on instance of the resource 
            if len(cityResources) == 2:
                return True 
        if len(self.location_to_build_settlement()) == 0:
            settlementResources = ['hay', 'brick', 'wood', 'sheep']
            for resource in self.game.currentPlayer.resources:
                if resource in settlementResources:
                    settlementResources.remove(resource) # will remove on instance of the resource 
            if len(settlementResources) == 2:
                return True
        if 'brick' not in self.game.currentPlayer.resources and 'wood' not in self.game.currentPlayer.resources:
            return True
        return False 
        
    def decide_to_play_yop(self):
        if self.can_build_city():
            cityResources = ['hay', 'hay', 'hay', 'ore', 'ore']
            for resource in self.game.currentPlayer.resources:
                if resource in cityResources:
                    cityResources.remove(resource) # will remove on instance of the resource 
            if len(cityResources) == 2:
                self.game.state.yoPlenty.clear()
                for resource in cityResources:
                    self.game.state.yoPlenty.append(resource)
                return {'TYPE': 'prog',
                        'COMMAND': 'play year of plenty'}
        if self.len(self.location_to_build_settlement()) == 0:
            settlementResources = ['hay', 'brick', 'wood', 'sheep']
            for resource in self.game.currentPlayer.resources:
                if resource in settlementResources:
                    settlementResources.remove(settlementResources) # will remove on instance of the resource 
            if len(settlementResources) == 2:
                self.game.state.yoPlenty.clear()
                for resource in cityResources:
                    self.game.state.yoPlenty.append(resource)
                return {'TYPE': 'prog',
                        'COMMAND': 'play year of plenty'}
        if 'brick' not in self.game.currentPlayer.resources and 'wood' not in self.game.currentPlayer.resources:
            self.game.state.yoPlenty.clear()
            self.game.state.yoPlenty.append('brick')
            self.game.state.yoPlenty.append('wood')
            return {'TYPE': 'prog',
                    'COMMAND': 'play year of plenty'}
        
    def should_play_monopoly(self):
        for resource in resourceTypes:
            resourceCount = 0
            for player in self.game.players:
                resourceCount += player.resources.count(resource)
            if resourceCount > 5 and self.game.currentPlayer.resources.count(resource) <= 1:
                return True 
        return False 

    def decide_play_monopoly(self):
        resourcesAskFor = []
        maxResourceCount = 0
        for resource in resourceTypes:
            resourceCount = 0
            for player in self.game.players:
                resourceCount += player.resources.count(resource)
            if resourceCount > 5 and self.game.currentPlayer.resources.count(resource) <= 1:
                resourcesAskFor.append(resource)
                maxResourceCount = max(maxResourceCount, resourceCount)
        if len(resourcesAskFor)>1:
            #remove ones with fewer resources in game 
            for resource in resourcesAskFor:
                resourceCount = 0
                for player in self.game.players:
                    resourceCount += player.resources.count(resource)
                if resourceCount != maxResourceCount:
                    resourcesAskFor.remove(resource)
            while len(resourcesAskFor)>1:
                resourcesAskFor.remove(random.choice(resourcesAskFor))
        return {'TYPE': 'prog',
                'COMMAND': 'play monopoly',
                'RESOURCE' : resourcesAskFor[0]}

    def normal_turn(self):
        if self.robber_on_player_tile() and 'knight' in self.game.currentPlayer.getDevelopments():
            return {'TYPE': 'prog',
                'COMMAND': 'play knight'}
        elif self.can_build_city() and self.game.currentPlayer.sufficient_resources(['ore', 'ore', 'ore', 'hay', 'hay']):
            return self.try_to_build_city()
        elif self.can_build_settlement():
            return self.try_to_build_settlement()
        elif self.can_build_road() and len(self.location_to_build_settlement()) == 0 :
            return self.try_to_build_road()
        elif len(self.location_to_build_settlement()) == 0 and 'road building' in self.game.currentPlayer.getDevelopments():
            return {'TYPE': 'prog',
                'COMMAND': 'play road building'}
        elif self.can_buy_development() and len(self.game.developmentCards) > 0:
            return self.try_to_build_development_card()
        elif self.tradesProposedOnTurn.count('strike') < 2 and len(self.tradesProposedOnTurn)<3:
            return self.try_trade()
        elif 'year of plenty' in self.game.currentPlayer.getDevelopments() and self.should_play_yop():
            return self.decide_to_play_yop()
        elif 'monopoly' in self.game.currentPlayer.getDevelopments() and self.should_play_monopoly():
            return self.decide_play_monopoly()
        else:
            self.game.load_game_screen()
            return {'TYPE': 'prog',
                'COMMAND': 'end turn'}
        
    def turn(self):
        if self.game.state.currentScreen == 'place starting pieces':
            return self.starting_pieces()
        else:
            if not self.game.state.rolled:
                self.tradesProposedOnTurn.clear() 
                return {'TYPE': 'prog',
                        'COMMAND': 'roll dice'}
            elif self.game.state.currentScreen == 'robber placement':
                return self.decide_move_robber()
            elif self.game.state.currentScreen == 'robber steal':
                return self.decide_player_steal_from()
            elif self.game.state.currentScreen == 'discard':
                return self.decide_discard_cards()
            elif self.game.state.currentScreen == 'choose player to trade with':
                return self.who_to_trade_with()
            else:
                return self.normal_turn()