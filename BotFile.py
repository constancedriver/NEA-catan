import random
resourceTypes = ['sheep', 'hay', 'brick', 'wood', 'ore']
NodeToTiles = {}
NodeToResourceScore = {}
NodeToBuildScore = {}
tradesProposedOnTurn = [] #[get form trade, give into trade]

def get_existing_adjacent_nodes(node:tuple):
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

def get_resource_resource_score(resourceNum:int):
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
                     12:1}
    return ResourceScore[resourceNum]

def find_tiles_at_node(game:object,node:tuple):
    tiles = NodeToTiles.get(node, [])
    if len(tiles) == 0:
        for tile in game.tiles:
            if node in tile.getNodes():
                tiles.append(tile)
        NodeToTiles.update({node: tiles})
    return tiles

def find_harbour_at_node(game:object, node:tuple):
    for harbour in game.harbours:
        if node == harbour.getPosition():
            return harbour 
            # there can only ever be one harbour at a node 
            #this means it can immedately return when it finds a harbour at a node without loosing any harbours
    return None # if no harbour is found at the node

def find_node_resource_score(game:object, node:tuple):
    ResourceScore = NodeToResourceScore.get(node, 0)
    if ResourceScore == 0:
        #find each tile at the node
        for tile in find_tiles_at_node(game, node):
            #find resource number
            resNum = tile.getTileNum()
            ResourceScore += get_resource_resource_score(resNum)
        #finding if there is a harbour at the node
        harbour = find_harbour_at_node(game, node)
        if harbour != None:
            #3:1 (any) are worth 2 and all others are worth 1 point
            if harbour.getType() == 'any':
                ResourceScore += 2
            else:
                ResourceScore += 1
        NodeToResourceScore.update({node: ResourceScore})
    return ResourceScore

def decide_discard_cards(game:object):
    resources = game.players[game.turnIndex].resources.copy()
    numberToDiscard =  len(game.players[game.turnIndex].resources) // 2
    while len(resources) >  numberToDiscard:
        if can_build_city(game) and resources.count('hay') >= 2 and resources.count('ore') >= 3 and len(resources) >=  numberToDiscard+5:
            for i in range (0,2,1):
                resources.remove('hay')
                resources.remove('ore')
            resources.remove('ore')
        elif can_build_settlement(game) and 'hay' in resources and 'sheep' in resources and 'wood' in resources and 'brick' in resources and len(resources) >=  numberToDiscard+4:
            resources.remove('hay')
            resources.remove('brick')
            resources.remove('wood')
            resources.remove('sheep')
        elif can_build_road(game) and 'brick' in resources and 'wood' in resources and len(resources) >=  numberToDiscard+2:
            resources.remove('brick')
            resources.remove('wood')
        elif can_buy_development(game) and 'hay' in resources and 'sheep' in resources and 'ore' in resources and len(resources) >=  numberToDiscard+3:
            resources.remove('hay')
            resources.remove('ore')
            resources.remove('sheep')
        else:
            resources.remove(random.choice(resources))
    for resource in resources:
        game.state.discardCards.append(resource)
    return {'TYPE': 'prog',
            'COMMAND': 'discard cards'}

def decide_player_steal_from(game:object): 
    leastFavourableResourceScore = 12
    leastFavourablePlayer = []
    currentBot = game.players[game.turnIndex]
    # find lowest favour ResourceScore of players that can steal from
    players_can_steal_from = game.players_on_robber_tile()
    for player in players_can_steal_from:
        playerIndex = game.players.index(player)
        leastFavourableResourceScore = min(currentBot.get_favour_ResourceScore(playerIndex), leastFavourableResourceScore)
    # find which player(s) have this lowest ResourceScore
    for player in game.players_on_robber_tile():
        playerIndex = game.players.index(player)
        if currentBot.get_favour_ResourceScore(playerIndex) == leastFavourableResourceScore:
            leastFavourablePlayer.append(player)
    # if more than one least favoured, pick a random one of them
    return {'TYPE': 'prog',
            'COMMAND': 'steal from player',
            'INDEX': players_can_steal_from.index(random.choice(leastFavourablePlayer))}

def decide_move_robber(game:object):
    tileSettlements = []
    currentTurnColour = game.players[game.turnIndex].colour
    for tile in game.tiles:
        nodes = tile.getNodes()
        numberOfSettlements = 0
        for outpost in game.outposts:
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
                bestTileIndexResourceScore.append([i, get_resource_resource_score(game.tiles[i].getTileNum())])
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


def can_build_city(game:object):
    atLeastOneSettlement = False
    for outpost in game.players[game.turnIndex].outposts:
        if atLeastOneSettlement:
            break
        if not outpost.getisCity():
            atLeastOneSettlement = True
    if atLeastOneSettlement and game.players[game.turnIndex].sufficient_resources(['ore', 'ore', 'hay', 'hay', 'hay']):
        return True
    else:
        return False

def nowhere_to_build_settlement(game:object):
    legalNode = False # empty node at least one away from another outpost and attached to a road
    for road in game.players[game.turnIndex].roads:
        if legalNode:
            break 
        location = road.getLocation()
        if (not game.adjacent_to_settlement(location[0])) or (not game.adjacent_to_settlement(location[1])):
            legalNode = True
    return not legalNode

def can_build_settlement(game:object):
    if not nowhere_to_build_settlement(game) and game.players[game.turnIndex].sufficient_resources(['sheep', 'hay', 'brick', 'wood']):
        return True
    else:
        return False
    
def can_buy_development(game:object):
    if len(game.developmentCards) != 0 and game.players[game.turnIndex].sufficient_resources(['sheep', 'hay', 'ore']):
        return True
    else:
        return False
    
def can_build_road(game:object):
    if game.players[game.turnIndex].sufficient_resources(['wood', 'brick']):
        emptyEdge = False
        roads = game.players[game.turnIndex].roads
        # find is there is at least one road who has an empty adjacent edge
        for road in roads:
            if emptyEdge:
                break
            for location in road.getLocation():
                if emptyEdge:
                    break
                for node in game.get_adjacent_nodes(location):
                    if game.edge_empty([location, node]):
                        emptyEdge = True
                        break 
        return emptyEdge
    return False

def try_to_build_city(game:object):
    settlements = []
    for outpost in game.outposts:
        if outpost.getisCity():
            settlements.append(outpost)
    if len(settlements) != 0:
        ResourceScores = []
        for settlement in settlements:
            ResourceScores.append(find_node_resource_score(game, settlement.getLocation()))
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

def location_to_build_settlement(game:object):
    possibleLocations = []
    for road in game.players[game.turnIndex].roads:
        for location in road.getLocation():
            if game.node_empty(location) and not game.adjacent_to_settlement(location):
                possibleLocations.append(location)
    return possibleLocations

def try_to_build_settlement(game:object):
    highestResourceScore = 0
    possibleLocations = location_to_build_settlement(game)
    bestNodes = []
    for location in possibleLocations:
        highestResourceScore = max (highestResourceScore, find_node_resource_score(game, location))
    for node in possibleLocations:
        if find_node_resource_score(game, node) == highestResourceScore:
            bestNodes.append(node)
    if len(bestNodes) == 1:
        return {'TYPE': 'prog',
                'COMMAND': 'build',
                'NODES': [bestNodes[0], bestNodes[0]]} 
    else:  
        randomNode = random.choice(bestNodes)  
        return {'TYPE': 'prog',
                'COMMAND': 'build',
                'NODES': [randomNode, randomNode]} 

def try_to_build_road(game:object):
    allowsNewSettlement = allows_build_settlement(game)
    game.state.pressedNodes.clear()
    if len(allowsNewSettlement) == 1:
        for node in allowsNewSettlement[0]:
            game.state.pressedNodes.append(node)
    elif len(allowsNewSettlement) > 1:
        access = already_have_access(game)
        newNodes = []
        # find which of the nodes in the road is the new node 
        for road in allowsNewSettlement:
            for location in road:
                if location not in access:
                    newNodes.append(location)
        # find node(s) with best resource score
        maxResourceScore = 0
        for node in newNodes:
            maxResourceScore = max(maxResourceScore, find_node_resource_score(game, node))
        bestNodes = []
        for node in newNodes:
            if find_node_resource_score(game, node) == maxResourceScore:
                bestNodes.append(node)
        # choose a road with the best resource score and build it 
        chosenNode = random.choice(bestNodes)
        for road in allowsNewSettlement:
            if chosenNode in road:
                roadLoactions = road.getLocation()
                return {'TYPE': 'prog',
                'COMMAND': 'build',
                'NODES': [roadLoactions[0], roadLoactions[0]]} 
    else:
        # no roads create access to a new place to build a settlement 
        # choose a random road to build 
        randomRoad = random.choice(possible_road_locations(game))
        roadLoactions = randomRoad.getLocation()
        return {'TYPE': 'prog',
                'COMMAND': 'build',
                'NODES': [roadLoactions[0], roadLoactions[0]]} 

def allows_build_settlement(game:object):
    possibleLocations = possible_road_locations(game)
    access = already_have_access(game)
    allowsNewSettlement = []
    for roadLocation in possibleLocations:
        giveNewSettlement = False
        for node in roadLocation:
            if node not in access and not game.adjacent_to_settlement(node):
                giveNewSettlement = True
        if giveNewSettlement:
            allowsNewSettlement.append(roadLocation)
    return allowsNewSettlement

def possible_road_locations(game:object):
    access = already_have_access(game)
    possibleRoadLoactions = []
    for location in access: 
        adjacentNodes = get_existing_adjacent_nodes(location)
        for node in adjacentNodes:
            if game.edge_empty([location, node]):
                possibleRoadLoactions.append([location, node])
    return possibleRoadLoactions

def already_have_access(game:object):
    access = []
    for road in game.players[game.turnIndex].roads:
        for location in road.getLocation():
            if location not in access:
                access.append(location)
    return access

def try_to_build_development_card(game:object):
    if can_buy_development(game):  
        return {'TYPE': 'prog',
                'COMMAND': 'buy development'}
    
def trade_with_bank(game:object, resourceWant:str, resourceGiveAway:str):
    harbours = game.trade_with_harbour()
    numberGive = 0
    if resourceGiveAway in harbours:
        numberGive += 2
    elif 'any' in harbours:
        numberGive += 3
    else:
        numberGive += 4
    for i in range (0,numberGive,1):
        game.state.tradeOfferTurn.append(resourceGiveAway)
    game.state.tradeOfferOthers.append(resourceWant)
    return {'TYPE': 'prog',
            'COMMAND': 'trade with bank'}

    
def try_trade(game:object):
    global tradesProposedOnTurn
    mostWantedNumber = 0
    mostWantedResource = []
    couldTrade = []
    infomation = what_to_trade(game)
    dontTrade = infomation[0]
    want = infomation[1]
    if len(want) == 0: # no point in trading 
        tradesProposedOnTurn.append('strike')
        tradesProposedOnTurn.append('strike')
        #after two strikes the bot will stop proposing trades
    else: 
        playerResources = game.players[game.turnIndex].resources
        #decide which resource to trade based on which was wanted the most number of times
        for resource in resourceTypes:
            mostWantedNumber = max(mostWantedNumber, want.count(resource))
        for resource in resourceTypes:
            if want.count(resource) and mostWantedNumber != 0:
                mostWantedResource.append(resource)
        while len(mostWantedResource) > 1:
            mostWantedResource.remove(random.choice(mostWantedResource))
        #decide which resource to give away in the trade
        harbours = game.trade_with_harbour()
        for resource in resourceTypes:
            if playerResources.count(resource)>=dontTrade.count(resource)+4 or ('any' in harbours and playerResources.count(resource)>=dontTrade.count(resource)+3) or (resource in harbours and playerResources.count(resource)>=dontTrade.count(resource)+2):
                # can trade wiht bank 
                return trade_with_bank(game, mostWantedResource[0], resource)
            elif playerResources.count(resource)>dontTrade.count(resource):
                couldTrade.append(resource)
        for item in couldTrade:
            if [mostWantedResource[0], item] in tradesProposedOnTurn:
                #removing trades offers that have already been done 
                couldTrade.remove(item)
        if len(couldTrade) == 0:
            tradesProposedOnTurn.append('strike')#after two strikes the bot will stop proposing trades
        else:
            while len(couldTrade)>1:
                couldTrade.remove(random.choice(couldTrade))
            #add to list of trades proposed
            tradesProposedOnTurn.append([mostWantedResource[0], couldTrade[0]])
            #propose trade
            game.state.tradeOfferTurn.append(couldTrade[0])
            game.state.tradeOfferOthers.append(mostWantedResource[0])
            return {'TYPE': 'prog',
                'COMMAND': 'trade with player'}

def what_to_trade(game:object):
    resources = game.players[game.turnIndex].resources
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

def calculate_trade_score(game:object, player:object):
    score = 0
    #add favour score 
    score += game.players[game.turnIndex].get_favour_score(game.players[game.turnIndex].index(player))
    #take away number of VP /2
    score -= player.VP
    return score

def who_to_trade_with(game:object, playersAccepted:list):
    playersAccepted = game.acceptedTrade
    bestScore = calculate_trade_score(playersAccepted[0]) #ensures starting score isnt too high
    bestPlayers = []
    # find player(s) with best trade score
    for player in playersAccepted:
        tradeScore = calculate_trade_score(player)
        if bestScore < tradeScore:
            bestScore == tradeScore
            bestPlayers.clear()
            bestPlayers.append(player)
        elif bestScore == tradeScore:
            bestPlayers.append(player)
    return {'TYPE': 'prog',
            'COMMAND': 'choose player trade',
            'INDEX' : playersAccepted.index(random.choice(bestPlayers))}

def get_tiles_at_node(game:object, node:tuple):
    tilesAtNode = []
    for tile in game.tiles:
        if node in tile.getNodes():
            tilesAtNode.append(tile)
    return tilesAtNode

def get_starting_score(game:object,node:tuple):
    score = find_node_resource_score(game, node)
    resourcesAtNode = []
    for tile in get_tiles_at_node(game, node):
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

def starting_pieces(game:object):
    numberOfRoads = len(game.players[game.turnIndex].roads)
    numberofOutposts = len(game.players[game.turnIndex].outposts)
    if numberOfRoads == numberofOutposts:
        #place a settlement
        bestScore = 0
        bestNodes = []
        for tile in game.tiles:
            for node in tile.getNodes():
                #if a legal place to play
                if game.node_empty(node) and not game.adjacent_to_settlement(node):
                    startingScore = get_starting_score(node)
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
        for outpost in game.players[game.turnIndex].outposts:
            roadAttached = False
            outpostLocation = outpost.getLocation()
            for road in game.players[game.turnIndex].roads:
                if outpostLocation in road.getLocation():
                    roadAttached = True
            if not roadAttached:
                settlementToBuildFrom = outpostLocation
                #beacuse of the way the game set up works, one of the settlements wont have an attached road
        return {'TYPE': 'prog',
                'COMMAND': 'build',
                'NODES': [settlementToBuildFrom, random.choice(get_existing_adjacent_nodes(settlementToBuildFrom))]} 
        
def robber_on_player_tile(game:object):
    if game.players[game.turnIndex].colour in game.players_on_robber_tile():
        return True
    else:
        return False
    
def normal_turn(game:object):
    if robber_on_player_tile(game) and 'knight' in game.players[game.turnIndex].getDevelopments():
        return {'TYPE': 'prog',
            'COMMAND': 'play knight'}
    elif can_build_city(game):
        return try_to_build_city(game)
    elif can_build_settlement(game):
        return try_to_build_settlement(game)
    elif can_build_road(game) and nowhere_to_build_settlement(game):
        return try_to_build_road(game)
    elif nowhere_to_build_settlement(game) and 'road building' in game.players[game.turnIndex].getDevelopments():
        return {'TYPE': 'prog',
            'COMMAND': 'play road building'}
    elif can_buy_development(game) and len(game.developmentCards) > 0:
        return try_to_build_development_card(game)
    elif tradesProposedOnTurn.count('strike') < 2:
        return try_trade(game)
    else:
        return {'TYPE': 'prog',
            'COMMAND': 'end turn'}
    
def turn(game:object):
    if game.state.currentScreen == 'place starting pieces':
        return starting_pieces(game)
    else:
        if not game.state.rolled:
            global tradesProposedOnTurn
            tradesProposedOnTurn.clear() 
            return {'TYPE': 'prog',
                    'COMMAND': 'roll dice'}
        elif game.state.currentScreen == 'robber placement':
            return decide_move_robber(game)
        elif game.state.currentScreen == 'robber steal':
            return decide_player_steal_from(game)
        elif game.state.currentScreen == 'discard':
            return decide_discard_cards(game)
        else:
            return normal_turn(game)