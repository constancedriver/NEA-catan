import time
import pieces
import playerHand
import resourceTiles
import gui
import game

class GameState:
    def __init__ (self,currentState:str, pressedNodes=[], rolled:bool=False, tradeOfferTurn=[], tradeOfferOthers=[], acceptedTrade=[], yoPlenty=[]):
        self.currentState=currentState
        self.pressedNodes = pressedNodes
        self.rolled = rolled
        self.tradeOfferTurn = tradeOfferTurn
        self.tradeOfferOthers = tradeOfferOthers
        self.acceptedTrade = acceptedTrade
        self.yoPlenty = yoPlenty
    
    def convert_gui_coordinates_back(guiCoordinate):
        revertedCoordinate= {(619.94,285): (5,3,2),
                            (619.94,375): (4,3,2),
                            (542,420)   : (4,2,2),
                            (464.06,375): (4,2,3),
                            (464.06,285): (5,2,3),
                            (542,240)   : (5,3,3),
                            (777.94,285): (5,4,1),
                            (777.94,375): (4,4,1),
                            (700,420)   : (4,3,1),
                            (700,240)   : (5,4,2),
                            (935.94,285): (5,5,0),
                            (935.94,375): (4,5,0),
                            (858,420)   : (4,4,0),
                            (858,240)   : (5,5,1),
                            (541.94,510): (3,2,2),
                            (464,555)   : (3,1,2),
                            (386.06,510): (3,1,3),
                            (386.06,420): (4,1,3),
                            (699.94,510): (3,3,1),
                            (622,555)   : (3,2,1),
                            (857.94,510): (3,4,0),
                            (780,555)   : (3,3,0),
                            (1015.94,420):(4,5,-1),
                            (1015.94,510):(3,5,-1),
                            (938,555)   : (3,4,-1),
                            (462.94,645): (2,1,2),
                            (385,690)   : (2,0,2),
                            (307.06,645): (2,0,3),
                            (307.06,555): (3,0,3),
                            (620.94,645): (2,2,1),
                            (543,690)   : (2,1,1),
                            (778.94,645): (2,3,0),
                            (701,690)   : (2,2,0),
                            (936.94,645): (2,4,-1),
                            (859,690)   : (2,3,-1),
                            (1094.94,555):(3,5,-2),
                            (1094.94,645):(2,5,-2),
                            (1017,690)  : (2,4,-2),
                            (541.94,780): (1,1,1),
                            (464,825)   : (1,0,1),
                            (386.06,780): (1,0,2),
                            (699.94,780): (1,2,0),
                            (622,825)   : (1,1,0),
                            (857.94,780): (1,3,-1),
                            (780,825)   : (1,2,-1),
                            (1015.94,780):(1,4,-2),
                            (938,825)   : (1,3,-2),
                            (619.94,915): (0,1,0),
                            (542,960)   : (0,0,0),
                            (464.06,915): (0,0,1),
                            (777.94,915): (0,2,-1),
                            (700,960)   : (0,1,-1),
                            (935.94,915): (0,3,-2),
                            (858,960)   : (0,2,-2)
                            }
        return revertedCoordinate[guiCoordinate]
    
    def build(self):
        node1 = self.pressedNodes[0]
        node2 = self.pressedNodes[1]
        self.pressedNodes = []
        if node1 == node2:
            game.buildOutpost(self.convert_gui_coordinates_back(node1))
        else:
            game.buildRoad((self.convert_gui_coordinates_back(node1),self.convert_gui_coordinates_back(node2)))

    def load_game_screen(self):
        self.currentState = 'game'
################################

    def get_command(self):
        command = gui.command(self.currentState)
        if type(command) == str:
            # all screens/rules screen 
            if command == 'rules':
                gui.rules_screen()
            elif command == 'exit rules':
                if self.currentState == 'game':
                    self.load_game_screen()
                elif self.currentState == 'trade':
                    gui.trade_screen()
                elif self.currentState == 'development':
                    gui.development_screen()
            
            # game screen
            elif command == 'roll dice':
                game.game1.roll_dice()
            elif command == 'trade':
                self.currentState = 'trade'
                self.tradeOfferOthers = []
                self.tradeOfferTurn = []
                gui.trade_screen()
            elif command == 'development':
                self.currentState = 'development'
                self.yoPlenty = []
                gui.development_screen()
            elif command == 'end turn':
                game.game1.next_turn()
                gui.new_turn(game.game1.turnIndex, game.game1.players[game.game1.turnIndex])

            # development screen
            elif command == 'play knight':
                game.game1.play_knight()
            elif command == 'play road building':
                game.game1.play_road_building()

            elif command == 'play monopoly wood':
                game.game1.play_monopoly('wood')
            elif command == 'play monopoly brick':
                game.game1.play_monopoly('brick')
            elif command == 'play monopoly sheep':
                game.game1.play_monopoly('sheep')
            elif command == 'play monopoly hay':
                game.game1.play_monopoly('hay')
            elif command == 'play monopoly ore':
                game.game1.play_monopoly('ore')
            
            elif command == 'year of plenty add wood':
                if len(self.yoPlenty) < 2:
                    self.yoPlenty.append('wood')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'year of plenty add brick':
                if len(self.yoPlenty) < 2:
                    self.yoPlenty.append('brick')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'year of plenty add sheep':
                if len(self.yoPlenty) < 2:
                    self.yoPlenty.append('sheep')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'year of plenty add hay':
                if len(self.yoPlenty) < 2:
                    self.yoPlenty.append('hay')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'year of plenty add ore':
                if len(self.yoPlenty) < 2:
                    self.yoPlenty.append('ore')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'year of plenty remove wood':
                if 'wood' in self.yoPlenty:
                    self.yoPlenty.remove('wood')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'year of plenty remove brick':
                if 'brick' in self.yoPlenty:
                    self.yoPlenty.remove('brick')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'year of plenty remove sheep':
                if 'sheep' in self.yoPlenty:
                    self.yoPlenty.remove('sheep')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'year of plenty remove hay':
                if 'hay' in self.yoPlenty:
                    self.yoPlenty.remove('hay')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'year of plenty remove ore':
                if 'ore' in self.yoPlenty:
                    self.yoPlenty.remove('ore')
                    gui.update_year_of_plenty(self.yoPlenty)
            elif command == 'play year of pleanty complete':
                game.game1.play_year_of_plenty(self.yoPlenty)

            elif command == 'buy development':
                game.game1.create_development_card()
            elif command == 'load game screen':
                self.load_game_screen()
            

            # trade screen
            elif command == 'accept trade':
                self.acceptedTrade.append(player)
            elif command == 'decline trade':
                gui.askOtherPlayersForTrade(nextPlayer)
            elif command == 'cancel trade':
                self.tradeOfferOthers = []
                self.tradeOfferTurn = []
                self.load_game_screen()
            elif command == 'complete trade':
                pass 
            ######ask players

            # trade menu arrows
            if command == 'turn player: remove wood':
                if 'wood' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('wood')
                    gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'turn player: remove brick':
                if 'brick' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('brick')
                    gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'turn player: remove sheep':
                if 'sheep' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('sheep')
                    gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'turn player: remove hay':
                if 'hay' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('hay')
                    gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'turn player: remove ore':
                if 'ore' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('ore')
                    gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'turn player: add wood':
                self.tradeOfferTurn.append('wood')
                gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'turn player: add brick':
                self.tradeOfferTurn.append('brick')
                gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'turn player: add sheep':
                self.tradeOfferTurn.append('sheep')
                gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'turn player: add hay':
                self.tradeOfferTurn.append('hay')
                gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'turn player: add ore':
                self.tradeOfferTurn.append('ore')
                gui.reDrawTradeOfferYou(self.tradeOfferTurn, False)
            if command == 'other players: remove wood':
                if 'wood' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('wood')
                    gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
            if command == 'other players: remove brick':
                if 'brick' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('brick')
                    gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
            if command == 'other players: remove sheep':
                if 'sheep' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('sheep')
                    gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
            if command == 'other players: remove hay':
                if 'hay' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('hay')
                    gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
            if command == 'other players: remove ore':
                if 'ore' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('ore')
                    gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
            if command == 'other players: add wood':
                self.tradeOfferOthers.append('wood')
                gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
            if command == 'other players: add brick':
                self.tradeOfferOthers.append('brick')
                gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
            if command == 'other players: add sheep':
                self.tradeOfferOthers.append('sheep')
                gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
            if command == 'other players: add hay':
                self.tradeOfferOthers.append('hay')
                gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
            if command == 'other players: add ore':
                self.tradeOfferOthers.append('ore')
                gui.reDrawTradeOfferYou(self.tradeOfferOthers, True)
        else: # nodes pressed
            self.pressedNodes.append(command)
            gui.node_pressed(command)
            if len(self.pressedNodes) == 2:
                self.build()
        

