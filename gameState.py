import gui

class GameState:
    def __init__ (self,currentScreen:str='main menu', pressedNodes:list=[], rolled:bool=False, tradeOfferTurn:list=[], tradeOfferOthers:list=[], acceptedTrade:list=[], yoPlenty:list=[], discardCards:list=[], humans:int=4, bots:int=0, playerAsking:str='none', numberAsked:int=0):
        self.currentScreen = currentScreen
        self.pressedNodes = pressedNodes
        self.rolled = rolled
        self.tradeOfferTurn = tradeOfferTurn
        self.tradeOfferOthers = tradeOfferOthers
        self.acceptedTrade = acceptedTrade
        self.yoPlenty = yoPlenty # year of plenty
        self.discardCards = discardCards
        self.humans = humans
        self.bots = bots
        self.playerAsking = playerAsking
        self.numberAsked = numberAsked
    
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
            return [node1]
        else:
            return [node1,node2]

    def all_same_type(self, resourceList:list):
        oneType = False
        resources = ['wood', 'brick', 'sheep', 'hay', 'ore']
        for resource in resources:
            if resourceList.count(resource) == len(resourceList):
                oneType = True
        return oneType
    
    def trade_choice(self):
        if self.numberAsked > 3:
            colours = ['white', 'blue', 'red', 'orange']
            colours.remove(self.playerAsking)
            gui.ask_others_for_trade(colours[self.numberAsked])
        else:
            return self.acceptedTrade

    def get_command(self):
        command = gui.command(self.currentScreen)
        if type(command) == int:
            return command
        elif type(command) == str:
            # all screens/rules screen 
            if command == 'rules':
                gui.rules_screen()
            elif command == 'exit rules':
                if self.currentScreen == 'game':
                    self.load_game_screen()
                elif self.currentScreen == 'trade':
                    gui.trade_screen()
                elif self.currentScreen == 'development':
                    gui.development_screen()
            # main menu
            elif command == 'add human':
                if self.humans + self.bots < 4:
                    self.humans += 1
                    gui.update_humans(self.humans)
            elif command == 'add bot':
                if self.humans + self.bots < 4:
                    self.bots += 1
                    gui.update_bots(self.bots)
            elif command == 'remove human':
                if self.humans > 0:
                    self.humans -=1
                    gui.update_humans(self.humans)
            elif command == 'remove bot':
                if self.bots > 0:
                    self.bots -=1
                    gui.update_humans(self.bots)
            
            # game screen
            elif command == 'trade':
                self.currentScreen = 'trade'
                self.tradeOfferOthers = []
                self.tradeOfferTurn = []
                gui.trade_screen()
            elif command == 'development':
                self.currentScreen = 'development'
                self.yoPlenty = []
                gui.development_screen()
            
            # development screen
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
                if len(self.yoPlenty) == 2:
                    return ['year of plenty', self.yoPlenty]
            
            # discard card screen
            elif command == 'discard cards':
                command = ['discard', self.discardCards]
            # arrows 
            elif command == 'discard: remove wood':
                if 'wood' in self.discardCards:
                    self.discardCards.remove('wood')
                    gui.redraw_discard_cards(self.discardCards)
            elif command == 'discard: remove brick':
                if 'brick' in self.discardCards:
                    self.discardCards.remove('brick')
                    gui.redraw_discard_cards(self.discardCards)
            elif command == 'discard: remove sheep':
                if 'sheep' in self.discardCards:
                    self.discardCards.remove('sheep')
                    gui.redraw_discard_cards(self.discardCards)
            elif command == 'discard: remove hay':
                if 'hay' in self.discardCards:
                    self.discardCards.remove('hay')
                    gui.redraw_discard_cards(self.discardCards)
            elif command == 'discard: remove ore':
                if 'ore' in self.discardCards:
                    self.discardCards.remove('ore')
                    gui.redraw_discard_cards(self.discardCards)
            elif command == 'discard: add wood':
                self.discardCards.append('wood')
                gui.redraw_discard_cards(self.discardCards)
            elif command == 'discard: add brick':
                self.discardCards.append('brick')
                gui.redraw_discard_cards(self.discardCards)
            elif command == 'discard: add sheep':
                self.discardCards.append('sheep')
                gui.redraw_discard_cards(self.discardCards)
            elif command == 'discard: add hay':
                self.discardCards.append('hay')
                gui.redraw_discard_cards(self.discardCards)
            elif command == 'discard: add ore':
                self.discardCards.append('ore')
                gui.redraw_discard_cards(self.discardCards)
                
            # trade screen
            elif command == 'accept trade':
                self.acceptedTrade.append(True)
                self.asked_all_others()
            elif command == 'decline trade':
                self.acceptedTrade.append(False)
                self.asked_all_other()
            elif command == 'trade with bank':
                if len(self.tradeOfferOthers) == 1 and (2 <= len(self.tradeOfferTurn) <= 4):
                    if self.all_same_type(self.tradeOfferTurn):
                        command  = ['trade with bank', self.tradeOfferTurn[0], self.tradeOfferOthers[0]]
                    
            elif command == 'cancel trade':
                self.tradeOfferOthers = []
                self.tradeOfferTurn = []
                return 'load game screen'
            elif command == 'complete trade':
                command = ['complete trade', self.tradeOfferTurn, self.tradeOfferOthers]

            # trade menu arrows
            if command == 'turn player: remove wood':
                if 'wood' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('wood')
                    gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'turn player: remove brick':
                if 'brick' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('brick')
                    gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'turn player: remove sheep':
                if 'sheep' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('sheep')
                    gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'turn player: remove hay':
                if 'hay' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('hay')
                    gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'turn player: remove ore':
                if 'ore' in self.tradeOfferTurn:
                    self.tradeOfferTurn.remove('ore')
                    gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'turn player: add wood':
                self.tradeOfferTurn.append('wood')
                gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'turn player: add brick':
                self.tradeOfferTurn.append('brick')
                gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'turn player: add sheep':
                self.tradeOfferTurn.append('sheep')
                gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'turn player: add hay':
                self.tradeOfferTurn.append('hay')
                gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'turn player: add ore':
                self.tradeOfferTurn.append('ore')
                gui.redraw_trade_offer_you(self.tradeOfferTurn, False)
            if command == 'other players: remove wood':
                if 'wood' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('wood')
                    gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            if command == 'other players: remove brick':
                if 'brick' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('brick')
                    gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            if command == 'other players: remove sheep':
                if 'sheep' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('sheep')
                    gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            if command == 'other players: remove hay':
                if 'hay' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('hay')
                    gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            if command == 'other players: remove ore':
                if 'ore' in self.tradeOfferOthers:
                    self.tradeOfferOthers.remove('ore')
                    gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            if command == 'other players: add wood':
                self.tradeOfferOthers.append('wood')
                gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            if command == 'other players: add brick':
                self.tradeOfferOthers.append('brick')
                gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            if command == 'other players: add sheep':
                self.tradeOfferOthers.append('sheep')
                gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            if command == 'other players: add hay':
                self.tradeOfferOthers.append('hay')
                gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            if command == 'other players: add ore':
                self.tradeOfferOthers.append('ore')
                gui.redraw_trade_offer_you(self.tradeOfferOthers, True)
            else:
                return command
        else: # nodes pressed
            self.pressedNodes.append(command)
            gui.node_pressed(command)
            if len(self.pressedNodes) == 2:
                self.build()

