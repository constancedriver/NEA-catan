import random
import PlayerHandFile

class Bot():
    defaultPlayerFavour = [4,4,4]
    def __init__(self, ownIndex:int, playerFavour:list=None):
        self.playerFavour = playerFavour.copy() if playerFavour is not None else self.defaultPlayerFavour.copy()
        self.ownIndex = ownIndex

    def decrease_player_favour(self, playerIndex:int):
        if playerIndex > self.ownIndex:
            playerIndex -= 1
        if self.playerFavour[playerIndex] > 0:
            self.playerFavour[playerIndex] -= 1

    def increase_player_favour(self, playerIndex:int):
        if playerIndex > self.ownIndex:
            playerIndex -= 1
        self.playerFavour[playerIndex] += 1

    def accept_trade(self, playerIndex:int):
        if playerIndex > self.ownIndex:
            playerIndex -= 1
        chosenNum = random.randint(0, self.playerFavour[playerIndex]*2+2, 1)
        if chosenNum >= 6:
            return {'TYPE': 'prog',
                'COMMAND': 'trade choice',
                'CHOICE': True}
        else: 
            return {'TYPE': 'prog',
                'COMMAND': 'trade choice',
                'CHOICE': False}

    def bot_turn(self):
        canBuild = True
        while canBuild:
            if self.sufficient_resources(['ore', 'ore', 'ore', 'hay', 'hay']):
                self.try_to_build_city()
            elif self.sufficient_resources(['hay', 'brick', 'sheep', 'wood']):
                self.try_to_build_settlement()
            elif self.sufficient_resources(['brick', 'wood']):
                self.try_to_build_road()
            else:
                canBuild = False

    def find_node_score(self, node:tuple):
        score = 0
        #find each tile at the node
        #find resource number
        resNum = 0
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
        return score

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