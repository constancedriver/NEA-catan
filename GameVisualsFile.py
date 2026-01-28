import GuiFile

class GameVisuals:
    def __init__ (self, currentScreen:str='main menu', pressedNodes:list=[], rolled:bool=False,
                  tradeOfferTurn:list=[], tradeOfferOthers:list=[], acceptedTrade:list=[],
                  yoPlenty:list=[], discardCards:list=[], humans:int=4, bots:int=0,
                  playerAsking:str='none', numberAsked:int=0):
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
    
    def convert_gui_coordinates_back(self,guiCoordinate):
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
            GuiFile.ask_others_for_trade(colours[self.numberAsked])
        else:
            return self.acceptedTrade
        
    def exit_rules(self):
        if self.currentScreen == 'trade':
            GuiFile.trade_screen()
        elif self.currentScreen == 'development':
            GuiFile.development_screen()
        elif self.currentScreen == 'main menu':
            GuiFile.start_menu()
            GuiFile.update_bots(self.bots)
            GuiFile.update_humans(self.humans)

    def add_human(self):
        if self.humans + self.bots < 4:
            self.humans += 1
            GuiFile.update_humans(self.humans)

    def add_bot(self):
        if self.humans + self.bots < 4:
            self.bots += 1
            GuiFile.update_bots(self.bots)

    def remove_human(self):
        if self.humans > 0:
            self.humans -=1
            GuiFile.update_humans(self.humans)

    def remove_bot(self):
        if self.bots > 0:
            self.bots -=1
            GuiFile.update_bots(self.bots)

    def trade(self):
        print(self.rolled)
        if self.rolled:
            self.currentScreen = 'trade'
            self.tradeOfferOthers.clear()
            self.tradeOfferTurn.clear()
            GuiFile.trade_screen()

    def development(self):
        if self.rolled: 
            self.currentScreen = 'development'
            self.yoPlenty.clear()
            GuiFile.development_screen()
        
    def year_of_plenty_add(self,resource:str):
        if len(self.yoPlenty) < 2:
            self.yoPlenty.append(resource)
            GuiFile.update_year_of_plenty(self.yoPlenty)

    def year_of_plenty_remove(self, resource:str):
        if resource in self.yoPlenty:
                self.yoPlenty.remove(resource)
                GuiFile.update_year_of_plenty(self.yoPlenty)

    def discard_remove(self, resource:str):
        if resource in self.discardCards:
            self.discardCards.remove(resource)
            GuiFile.redraw_discard_cards(self.discardCards)

    def discard_add(self, resource:str):
        self.discardCards.append(resource)
        GuiFile.redraw_discard_cards(self.discardCards)

    def trade_turn_remove(self, resource:str):
        if resource in self.tradeOfferTurn:
            self.tradeOfferTurn.remove(resource)
            GuiFile.redraw_trade_offer_you(self.tradeOfferTurn, False)

    def trade_turn_add(self, resource:str):
        self.tradeOfferTurn.append(resource)
        GuiFile.redraw_trade_offer_you(self.tradeOfferTurn, False)

    def trade_others_remove(self, resource:str):
        if resource in self.tradeOfferOthers:
            self.tradeOfferOthers.remove(resource)
            GuiFile.redraw_trade_offer_you(self.tradeOfferOthers, True)

    def trade_others_add(self, resource:str):
        self.tradeOfferOthers.append(resource)
        GuiFile.redraw_trade_offer_you(self.tradeOfferOthers, True)

    def node_selected(self, node):
        if self.rolled or self.currentScreen == 'place starting pieces':
            self.pressedNodes.append(self.convert_gui_coordinates_back(node))
            GuiFile.node_pressed(node)

    def get_command(self,command):
        action = {'rules' : lambda:GuiFile.rules_screen(),
                  'exit rules': lambda:self.exit_rules(),
                  'add human': lambda:self.add_human(),
                  'add bot': lambda:self.add_bot(),
                  'remove human': lambda:self.remove_human(),
                  'remove bot': lambda:self.remove_bot(),
                  'trade': lambda:self.trade(),
                  'development' : lambda:self.development(),
                  'year of plenty add': lambda:self.year_of_plenty_add(command['RESOURCE']),
                  'year of plenty remove': lambda:self.year_of_plenty_remove(command['RESOURCE']),
                  'discard: remove': lambda:self.discard_remove(command['RESOURCE']),
                  'discard: add' : lambda:self.discard_add(command['RESOURCE']),
                  'turn player: remove': lambda:self.trade_turn_remove(command['RESOURCE']),
                  'turn player: add': lambda:self.trade_turn_add(command['RESOURCE']),
                  'other players: remove': lambda:self.trade_others_remove(command['RESOURCE']),
                  'other players: add': lambda:self.trade_others_add(command['RESOURCE']),
                  'node selected': lambda:self.node_selected(command['NODE'])}
        return action[command['COMMAND']]
    