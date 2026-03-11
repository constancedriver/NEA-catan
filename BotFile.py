import random

NodeToTiles = {}
NodeToScore = {}

def find_tiles_at_node(game,node):
    tiles = NodeToTiles.get(node, [])
    if len(tiles) == 0:
        for tile in game.tiles:
            if node in tile.getNodes():
                tiles.append(tile)
        NodeToTiles.update({node: tiles})
    return tiles

def find_node_score(game, node:tuple):
        score = NodeToScore.get(node, 0)
        if score == 0:
            #find each tile at the node
            for tile in find_tiles_at_node(game, node):
                #find resource number
                resNum = tile.getTileNum
                #calculate probaility of producing a resource
                if resNum == 6 or resNum == 8:
                    score += 5
                elif resNum == 5 or resNum == 9:
                    score += 4
                elif resNum == 4 or resNum == 10:
                    score += 3
                elif resNum == 3 or resNum == 11:
                    score += 2
                elif resNum == 2 or resNum == 12:
                    score += 1
            NodeToScore.update({node: score})
        return score

def turn(game):
    if game.state.currentScreen == 'place starting pieces':
        starting_pieces(game)
    else:
        if game.state.rolled:
            normal_turn(game)
        elif game.state.currentScreen == 'robber placement':
            decide_move_robber(game)
        elif game.state.currentScreen == 'robber steal':
            decide_player_steal_from(game)
        elif game.state.currentScreen == 'discard':
            decide_discard_cards(game)
        else:
            return {'TYPE': 'prog',
                    'COMMAND': 'roll dice'}

def decide_player_steal_from(game): 
    leastFavourableScore = 12
    leastFavourableScore
    currentBot = game.players[game.turnIndex]
    for player in game.players_on_robber_tile():
        playerIndex = game.players.index(player)
        leastFavourableScore = min(currentBot.get_favour_score(playerIndex), leastFavourableScore)


def starting_pieces(game):
    if len(game.players[game.turnIndex].outposts) != len(game.players[game.turnIndex].roads):
        # in the game set up if a player doesnt have equal number of roads and settlememts then they have to play a settlement 
        pass

def can_build_city(game):
    atLeastOneSettlement = False
    for outpost in game.players[game.turnIndex].outposts:
        if atLeastOneSettlement:
            break
        if outpost.getisCity():
            atLeastOneSettlement = True
    if atLeastOneSettlement and game.players[game.turnIndex].sufficient_resources(['ore', 'ore', 'wheat', 'wheat', 'wheat']):
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
    if legalNode and game.players[game.turnIndex].sufficient_resources(['sheep', 'wheat', 'brick', 'wood']):
        return True
    else:
        return False
    
def can_buy_development(game):
    if len(game.developmentCards) != 0 and game.players[game.turnIndex].sufficient_resources(['sheep', 'wheat', 'ore']):
        return True
    else:
        return False
    
def can_build_road(game):
    pass

def try_to_build_city(self):
    settlements = []
    for outpost in self.outposts:
        if outpost.getisCity():
            settlements.append(outpost)
    if len(settlements) != 0:
        scores = []
        for settlement in settlements:
            scores.append(self.find_node_score(settlement.getLocation()))
        highestScore=0
        for i in range (0,len(settlements),1):
            highestScore = max(scores[i], highestScore)
        if scores.count(highestScore) == 1:
            settlementIndex = scores.index(highestScore)    
        else:
            # will pick a random settlemnt with the highest score
            possibleIndexes = []
            for i in range (0,len(scores),1):
                if scores[i] == highestScore:
                    possibleIndexes.append(i)
            settlementIndex = random.choice(possibleIndexes)
        node = settlements[settlementIndex].getLocation()
        return {'TYPE': 'prog',
                'COMMAND': 'build',
                'NODES': [node, node]}

def try_to_build_settlement(self):
    pass

def try_to_build_road(self):
    pass

def try_trade(self):
    pass

def try_trade_with_harbours(self):
    pass