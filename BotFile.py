import random
board = {}
def make_board(game):
    for tile in game.tiles:
        nodes = tile.getNodes()
        for node in nodes:
            if board.get(node, None) == None:
                board.update({node: game.get_adjacent_nodes(node)})


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
NodeToTiles = {}
NodeToResourceScore = {}

def find_tiles_at_node(game,node:tuple):
    tiles = NodeToTiles.get(node, [])
    if len(tiles) == 0:
        for tile in game.tiles:
            if node in tile.getNodes():
                tiles.append(tile)
        NodeToTiles.update({node: tiles})
    return tiles

def find_harbour_at_node(game, node:tuple):
    for harbour in game.harbours:
        if node == harbour.getPosition():
            return harbour 
            # there can only ever be one harbour at a node 
            #this means it can immedately return when it finds a harbour at a node without loosing any harbours
    return None # if no harbour is found at the node

def find_node_resource_score(game, node:tuple):
        ResourceScore = NodeToResourceScore.get(node, 0)
        if ResourceScore == 0:
            #find each tile at the node
            for tile in find_tiles_at_node(game, node):
                #find resource number
                resNum = tile.getTileNum
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

def turn(game):
    if game.state.currentScreen == 'place starting pieces':
        starting_pieces(game)
    else:
        if not game.state.rolled:
            return {'TYPE': 'prog',
                    'COMMAND': 'roll dice'}
        elif game.state.currentScreen == 'robber placement':
            decide_move_robber(game)
        elif game.state.currentScreen == 'robber steal':
            decide_player_steal_from(game)
        elif game.state.currentScreen == 'discard':
            decide_discard_cards(game)
        else:
            normal_turn(game)

def decide_discard_cards(game):
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
        else:
            card = random.choice(resources)
            resources.remove(card)
    for resource in resources:
        game.state.discardCards.append(resource)
    return {'TYPE': 'prog',
            'COMMAND': 'discard cards'}

def decide_player_steal_from(game): 
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
    while len(leastFavourablePlayer) > 1:
        leastFavourablePlayer.pop(random.randint(0,len(leastFavourablePlayer)-1))
    return {'TYPE': 'prog',
            'COMMAND': 'steal from player',
            'INDEX': players_can_steal_from.index(leastFavourablePlayer)}

def decide_move_robber(game):
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


def can_build_city(game):
    atLeastOneSettlement = False
    for outpost in game.players[game.turnIndex].outposts:
        if atLeastOneSettlement:
            break
        if outpost.getisCity():
            atLeastOneSettlement = True
    if atLeastOneSettlement and game.players[game.turnIndex].sufficient_resources(['ore', 'ore', 'hay', 'hay', 'hay']):
        return True
    else:
        return False
    
def can_build_settlement(game):
    legalNode = False # empty node at least one away from another outpost and attached to a road
    for road in game.players[game.turnIndex].roads:
        if legalNode:
            break 
        location = road.getLocation()
        if game.node_empty(location[0]) and game.node_empty(location[1]):
            legalNode = True
    if legalNode and game.players[game.turnIndex].sufficient_resources(['sheep', 'hay', 'brick', 'wood']):
        return True
    else:
        return False
    
def can_buy_development(game):
    if len(game.developmentCards) != 0 and game.players[game.turnIndex].sufficient_resources(['sheep', 'hay', 'ore']):
        return True
    else:
        return False
    
def can_build_road(game):
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

def try_to_build_city(game):
    settlements = []
    for outpost in game.outposts:
        if outpost.getisCity():
            settlements.append(outpost)
    if len(settlements) != 0:
        ResourceScores = []
        for settlement in settlements:
            ResourceScores.append(game.find_node_resource_score(settlement.getLocation()))
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

def location_to_build_settlement(game):
    possibleLocations = []
    for road in game.players[game.turnIndex].roads:
        for location in road.getLocation():
            if game.node_empty(location) and not game.adjacent_to_settlement(location):
                possibleLocations.append(location)
    return possibleLocations

def try_to_build_settlement(game):
    highestResourceScore = 0
    possibleLocations = location_to_build_settlement(game)
    bestNodes = []
    for location in possibleLocations:
        highestResourceScore = max (highestResourceScore, find_node_resource_score(location))
    for node in possibleLocations:
        if find_node_resource_score(node) == highestResourceScore:
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

def try_to_build_development_card(game):
    if can_buy_development(game):
        return {'TYPE': 'prog',
                'COMMAND': 'buy development'}

def try_to_build_road(game):
    pass

def try_trade(game):
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
    if len(want) >0: # otherwise no point in trading
        highestWantCount = 0
        highestWantResource = []
        resourceTypes = ['ore', 'sheep', 'hay', 'wood', 'brick']
        for resource in resourceTypes:
            highestWantCount = max(highestWantCount, want.count(resource))
        for resource in resourceTypes:
            if want.count(resource) == highestWantCount:
                highestWantResource.append(resource)
        if len(highestWantResource) == 1:
            pass
####################################################################################################
def try_trade_with_harbours(game):
    pass

def trade_successful(game):
    return False
    pass

def starting_pieces(game):
    if len(game.players[game.turnIndex].outposts) != len(game.players[game.turnIndex].roads):
        # in the game set up if a player doesnt have equal number of roads and settlememts then they have to play a settlement 
        pass

def normal_turn(game):
    tryingToBuild = True
    while tryingToBuild:
        if can_build_city(game):
            try_to_build_city(game)
        elif can_build_settlement(game):
            try_to_build_settlement(game)
        elif can_build_road(game):
            try_to_build_road(game)
        elif can_buy_development(game):
            try_to_build_development_card(game)
        else:
            tryingToBuild = False
    if trade_successful(game):
        normal_turn(game)
    else:
        return {'TYPE': 'prog',
            'COMMAND': 'end turn'}