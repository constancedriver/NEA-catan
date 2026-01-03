import pygame
import math
import time
pygame.font.init()

WIDTH, HEIGHT = 1400, 1200
HEX_RADIUS = 90
CIRCLE_RADIUS = 35
SMALLFONT = pygame.font.SysFont('Corbel',35)

#coordinate system (created by me) used in the game file converted to the actual coordinated on the screen

def convert_coordinates(n):
    a = {(5,3,2): (619.94,285),
         (4,3,2): (619.94,375),
         (4,2,2): (542,420),
         (4,2,3): (464.06,375),
         (5,2,3): (464.06,285),
         (5,3,3): (542,240),
         (5,4,1): (777.94,285),
         (4,4,1): (777.94,375),
         (4,3,1): (700,420),
         (5,4,2): (700,240),
         (5,5,0): (935.94,285),
         (4,5,0): (935.94,375),
         (4,4,0): (858,420),
         (5,5,1): (858,240),
         (3,2,2): (541.94,510),
         (3,1,2): (464,555),
         (3,1,3): (386.06,510),
         (4,1,3): (386.06,420),
         (3,3,1): (699.94,510),
         (3,2,1): (622,555),
         (3,4,0): (857.94,510),
         (3,3,0): (780,555),
         (4,5,-1): (1015.94,420),
         (3,5,-1): (1015.94,510),
         (3,4,-1): (938,555),
         (2,1,2): (462.94,645),
         (2,0,2): (385,690),
         (2,0,3): (307.06,645),
         (3,0,3): (307.06,555),
         (2,2,1): (620.94,645),
         (2,1,1): (543,690),
         (2,3,0): (778.94,645),
         (2,2,0): (701,690),
         (2,4,-1): (936.94,645),
         (2,3,-1): (859,690),
         (3,5,-2): (1094.94,555),
         (2,5,-2): (1094.94,645),
         (2,4,-2): (1017,690),
         (1,1,1): (541.94,780),
         (1,0,1): (464,825),
         (1,0,2): (386.06,780),
         (1,2,0): (699.94,780),
         (1,1,0): (622,825),
         (1,3,-1): (857.94,780),
         (1,2,-1): (780,825),
         (1,4,-2): (1015.94,780),
         (1,3,-2): (938,825),
         (0,1,0): (619.94,915),
         (0,0,0): (542,960),
         (0,0,1): (464.06,915),
         (0,2,-1): (777.94,915),
         (0,1,-1): (700,960),
         (0,3,-2): (935.94,915),
         (0,2,-2): (858,960)}
    return a[n]

#  Resource colors 
def get_colour(colourName):
    colourDef = {
    'wood' :(0, 105, 0),#(34, 139, 34),      
    'hay':  (255, 229, 33),     
    'brick':(182, 68, 7),     
    'sheep':(70, 190, 0),#(148, 207, 0),      
    'ore':  (97, 97, 97),       
    'none': (204, 173, 96),
    'any': (115, 0, 255), 
    'red':  (255, 0, 0),
    'blue': (0, 0, 255),
    'white':(255,225,255),
    'orange':(255, 147, 0)}
    return colourDef[colourName]

def get_resource_colours(): # add tiles as parameter
    resources = []
    #for tile in tiles:
    #    resources.append(tile.resource)
    resources = ['ore', 'sheep', 'wood', 'hay', 'brick', 'sheep', 'brick', 'hay', 'wood', 'none', 'wood', 'ore', 'wood', 'ore', 'hay', 'sheep', 'brick', 'hay', 'sheep']
    colours = []
    for resource in resources:
        colours.append(get_colour(resource))
        #colours.append(get_colour(tile.resource))
    return colours

def draw_hex(surface, color, center, radius):
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, (0, 0, 0), points, 3)

def draw_center_circle(surface, center, radius):
    pygame.draw.circle(surface, (204, 173, 96), center, radius)  

def generate_catan_layout(center_x, center_y): # add tiles as parameter
    colours = get_resource_colours() # add tiles as parameter
    layout = []
    rows = [3, 4, 5, 4, 3]
    h_spacing = HEX_RADIUS * 1.75
    v_spacing = HEX_RADIUS * 1.5

    y_offset = center_y - v_spacing * 2
    j = 0
    for count in rows:
        x_offset = center_x - (count - 1) * h_spacing / 2
        for i in range(count):
            layout.append((
                (int(x_offset + i * h_spacing), int(y_offset)),
                colours[j]
            ))
            j += 1
        y_offset += v_spacing

    return layout

def update_longest_road(player):
    colour = players[player]
    pygame.draw.rect(screen, get_colour(colour), (34,510,149,30))
    pygame.display.update(34,510,149,30)

def update_largest_army(player):
    colour = players[player]
    pygame.draw.rect(screen, get_colour(colour), (34,580,149,30))
    pygame.display.update(34,580,149,30)

def new_turn(turnIndex, resources=[], developmentCards=[], roadsLeft=0, settlementsLeft=0, citiesLeft=0, knightsPlayed=0): # !!!!!!!!!!!!!!!! INPUT PLAYER HAND PROPERTIES!!!!!!!!!!!!!
    colour = players[turnIndex]
    pygame.draw.rect(screen, get_colour(colour), (283,1000, 834, 100))
    pygame.draw.rect(screen, get_colour(colour), (283,0, 834, 200))
    pygame.draw.rect(screen, get_colour('wood'), (316,20,127.2,50))
    pygame.draw.rect(screen, get_colour('brick'), (476.2,20,127.2,50))
    pygame.draw.rect(screen, get_colour('sheep'), (636.4,20,127.2,50))
    pygame.draw.rect(screen, get_colour('hay'), (796.6,20,127.2,50))
    pygame.draw.rect(screen, get_colour('ore'), (956.8,20,127.2,50))
    screen.blit((SMALLFONT.render(str(resources.count('wood')) , True , (0,0,0))), (373,30))
    screen.blit((SMALLFONT.render(str(resources.count('brick')) , True , (0,0,0))), (533,30))
    screen.blit((SMALLFONT.render(str(resources.count('sheep')) , True , (0,0,0))), (693,30))
    screen.blit((SMALLFONT.render(str(resources.count('hay')) , True , (0,0,0))), (854,30))
    screen.blit((SMALLFONT.render(str(resources.count('ore')) , True , (0,0,0))), (1014,30))
    screen.blit((SMALLFONT.render(('roads left:'+str(roadsLeft)) , True , (0,0,0))), (316,130))
    screen.blit((SMALLFONT.render(('settlements left:'+str(settlementsLeft)) , True , (0,0,0))), (716,130))
    screen.blit((SMALLFONT.render(('cities left:'+str(citiesLeft)) , True , (0,0,0))), (316,160))
    screen.blit((SMALLFONT.render(('knights played:'+str(knightsPlayed)) , True , (0,0,0))), (716,160))
    screen.blit((SMALLFONT.render(('dev:') , True , (0,0,0))), (316,80))
    i = 1
    for card in developmentCards:
        screen.blit((SMALLFONT.render((card) , True , (0,0,0))), (316+100*i,80))
        i+=1
    pygame.display.update(283,1000, 834, 100)
    pygame.display.update(283,0, 834, 200)

def draw_player_banners(players):
    pygame.draw.rect(screen, get_colour(players[0]), (1183, 20, 183, 193))
    pygame.draw.rect(screen, get_colour(players[1]), (1183, 233, 183, 193))
    pygame.draw.rect(screen, get_colour(players[2]), (1183, 446, 183, 193))
    pygame.draw.rect(screen, get_colour(players[3]), (1183, 659, 183, 193))
    pygame.display.update(1183, 20, 183, 1150)

def display_dice(dice1, dice2):
    screen.blit((SMALLFONT.render(str(dice1) , True , (0,0,0))), (1214,909))
    screen.blit((SMALLFONT.render(str(dice2) , True , (0,0,0))), (1322,909))
    pygame.display.update(1183, 884, 183, 75)

def create_hex_node_buttons():
    hex_node_coordinates = [(619.94,285),(619.94,375),(542,420),(464.06,375),(464.06,285),(542,240),(777.94,285),(777.94,375),(700,420),(700,240),(935.94,285),(935.94,375),(858,420),(858,240),(541.94,510),(464,555),(386.06,510),(386.06,420),(699.94,510),(622,555),(857.94,510),(780,555),(1015.94,420),(1015.94,510),(938,555),(462.94,645),(385,690),(307.06,645), (307.06,555),(620.94,645), (543,690),(778.94,645), (701,690),(936.94,645), (859,690),(1094.94,555), (1094.94,645),(1017,690),(541.94,780),(464,825), (386.06,780),(699.94,780), (622,825),(857.94,780), (780,825),(1015.94,780),(938,825), (619.94,915),(542,960),(464.06,915),(777.94,915),(700,960),(935.94,915), (858,960)]
    for node in hex_node_coordinates:
        pygame.draw.circle(screen, (0,0,0), node, 10, 2)

def draw_road(road):
    locations = road[0]
    colour = road[1]
    pygame.draw.lines(screen, get_colour(colour), False, (convert_coordinates(locations[0]),convert_coordinates(locations[1])), 10)
    create_hex_node_buttons()
    pygame.display.flip()

def draw_settlement(settlement):
    location = settlement[0]
    colour = settlement[1]
    x = convert_coordinates(location)[0]
    y = convert_coordinates(location)[1]
    pygame.draw.rect(screen, get_colour(colour), (x-15, y-15, 30, 30))
    pygame.draw.polygon(screen, get_colour(colour), ((x-15,y-15),(x+15,y-15),(x,y-22.5)))
    create_hex_node_buttons()
    pygame.display.update(x-15, y-22.5, 30, 37.5)

def draw_city(city):
    location = city[0]
    colour = city[1]
    x = convert_coordinates(location)[0]
    y = convert_coordinates(location)[1]
    draw_settlement(city)
    pygame.draw.rect(screen, get_colour(colour), (x-30, y-15, 15, 30))
    pygame.display.update(x-30, y-15, 15, 30)

def draw_harbours(harbours):
    for harbour in harbours:
        colour = get_colour(harbour[1])
        node = convert_coordinates(harbour[0])
        pygame.draw.circle(screen, colour, node, 25)

def draw_building_key():
    screen.blit((SMALLFONT.render('BUILDING KEY:' , True , (0,0,0))), (10,20))
    screen.blit((SMALLFONT.render('Road:' , True , (0,0,0))), (10,50))
    screen.blit((SMALLFONT.render('wood' , True , get_colour('wood'))), (10,80))
    screen.blit((SMALLFONT.render('brick' , True , get_colour('brick'))), (100,80))
    screen.blit((SMALLFONT.render('Settlement:      1VP' , True , (0,0,0))), (10,110))
    screen.blit((SMALLFONT.render('wood' , True , get_colour('wood'))), (10,140))
    screen.blit((SMALLFONT.render('brick' , True , get_colour('brick'))), (100,140))
    screen.blit((SMALLFONT.render('sheep' , True , get_colour('sheep'))), (10,170))
    screen.blit((SMALLFONT.render('wheat' , True , get_colour('hay'))), (100,170))
    screen.blit((SMALLFONT.render('City:            2VP' , True , (0,0,0))), (10,210))
    screen.blit((SMALLFONT.render('wheat' , True , get_colour('hay'))), (10,240))
    screen.blit((SMALLFONT.render('wheat' , True , get_colour('hay'))), (100,240))
    screen.blit((SMALLFONT.render('ore' , True , get_colour('ore'))), (10,270))
    screen.blit((SMALLFONT.render('ore' , True , get_colour('ore'))), (100,270))
    screen.blit((SMALLFONT.render('ore' , True , get_colour('ore'))), (200,270))
    screen.blit((SMALLFONT.render('Development Card:' , True , (0,0,0))), (10,300))
    screen.blit((SMALLFONT.render('sheep' , True , get_colour('sheep'))), (10,330))
    screen.blit((SMALLFONT.render('wheat' , True , get_colour('hay'))), (100,330))
    screen.blit((SMALLFONT.render('ore' , True , get_colour('ore'))), (200,330))
    screen.blit((SMALLFONT.render('dev cards cannot' , True , (0,0,0))), (10,360))
    screen.blit((SMALLFONT.render('be played on the ' , True , (0,0,0))), (10,380))
    screen.blit((SMALLFONT.render('turn they are bought' , True , (0,0,0))), (10,400))
    screen.blit((SMALLFONT.render('unless it is a VP' , True , (0,0,0))), (10,420))
    pygame.display.update(0,0,250,460)

def create_game_screen():
    resNum = ['5','6','11','8','3','4','5','9','11','','3','8','12','6','4','10','10','2','9']
    i = 0
    for hex_center, colour in board:
        draw_hex(screen, colour, hex_center, HEX_RADIUS)
        draw_center_circle(screen, hex_center, CIRCLE_RADIUS)
        screen.blit((SMALLFONT.render(str(resNum[i]) , True , (0,0,0))), (hex_center[0]-8,hex_center[1]-10))
        i += 1
    pygame.draw.rect(screen, (204, 173, 96), (0,0, 250, 1200))
    pygame.draw.rect(screen, (204, 173, 96), (1150,0, 250, 1200))
    pygame.draw.rect(screen, (255,255,255), (1183, 884, 75, 75))
    pygame.draw.rect(screen, (255,255,255), (1291, 884, 75, 75))
    pygame.draw.rect(screen, (255,0,0), (1183, 992, 183, 75))
    screen.blit((SMALLFONT.render('quit' , True , (0,0,0))), (1249,1017))
    pygame.draw.rect(screen, (255,255,255), (34, 992, 183, 75))
    pygame.draw.rect(screen, (255,255,255), (34, 884, 183, 75))
    pygame.draw.rect(screen, (255,255,255), (34, 776, 183, 75))
    pygame.draw.rect(screen, (255,255,255), (34, 668, 183, 75))
    screen.blit((SMALLFONT.render('rules' , True , (0,0,0))), (95,1017))
    screen.blit((SMALLFONT.render('end turn' , True , (0,0,0))), (75,909))
    screen.blit((SMALLFONT.render('trade' , True , (0,0,0))), (95,801))
    screen.blit((SMALLFONT.render('development' , True , (0,0,0))), (47,693))
    screen.blit((SMALLFONT.render('LARGEST ARMY:' , True , (0,0,0))), (10,550))
    screen.blit((SMALLFONT.render('LONGEST ROAD:' , True , (0,0,0))), (10,480))
    display_dice(0,0)
    create_hex_node_buttons()
    draw_building_key()
    pygame.display.flip()

def rules_screen():
    screen.fill((204, 173, 96))
    pygame.draw.rect(screen, (255,0,0), (1217, 0, 183, 75))
    screen.blit((SMALLFONT.render('back to game' , True , (0,0,0))), (1233,25))
    pygame.display.flip()
 #!!!!!###### print actual rules!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def trade_screen():
    screen.fill((204, 173, 96))
    pygame.draw.rect(screen, (255,0,0), (1217, 0, 183, 75))
    screen.blit((SMALLFONT.render('cancel trade' , True , (0,0,0))), (1233,25))
    pygame.draw.rect(screen, (0,255,0), (0, 0, 183, 75))
    screen.blit((SMALLFONT.render('complete trade' , True , (0,0,0))), (6,25))
    screen.blit((SMALLFONT.render('TRADE MENU' , True , (0,0,0))), (620,25))
    #creating cards
    pygame.draw.rect(screen, (get_colour('wood')), (34, 360, 240, 480))
    pygame.draw.rect(screen, (get_colour('brick')), (307, 360, 240, 480))
    pygame.draw.rect(screen, (get_colour('sheep')), (580, 360, 240, 480))
    pygame.draw.rect(screen, (get_colour('hay')), (853, 360, 240, 480))
    pygame.draw.rect(screen, (get_colour('ore')), (1126, 360, 240, 480))
    # creating arrows
    screen.blit((SMALLFONT.render('You put in:' , True , (0,0,0))), (100,150))
    screen.blit((SMALLFONT.render('Other players put in:' , True , (0,0,0))), (100,1000))
    for j in range (0,2,1):
        for i in range (0,5,1):
            screen.blit((SMALLFONT.render('0' , True , (0,0,0))), ((149+(i*273)),(280+(j*621))))
            pygame.draw.polygon(screen, (0,0,0), (((116.5+(i*273)),(327+(j*621))),((116.5+(i*273)),(252+(j*621))),((41+(i*273)),(289.5+(j*621))))) # down
            pygame.draw.polygon(screen, (0,0,0), (((195+(i*273)),(327+(j*621))),((195+(i*273)),(252+(j*621))),((267+(i*273)),(289.5+(j*621))))) # up
    pygame.display.flip()

def askOtherPlayersForTrade(playerTurn, players, playerToAsk):
    if playerToAsk != playerTurn:
        player = players[playerToAsk]
        pygame.draw.rect(screen, get_colour(player), (427,360,546,480))
        pygame.draw.rect(screen, (0,255,0), (460,393,223.5,414))
        pygame.draw.rect(screen, (255,0,0), (716.5,393,223.5,414))
        screen.blit((SMALLFONT.render('accept trade' , True , (0,0,0))), (470,400))
        screen.blit((SMALLFONT.render('decline trade' , True , (0,0,0))), (726.5,400))
        pygame.display.update(427,360,546,480)
            
def reDrawTradeOfferYou(tradeOffer, others=bool):
    resourceOrder = ['wood', 'brick', 'sheep', 'hay', 'ore']
    for i in range (0,5,1):
            pygame.draw.rect(screen, get_colour('none'), ((116.5+(i*273)),(252+(others*621)), 75,75))
            screen.blit((SMALLFONT.render(str(tradeOffer.count(resourceOrder[i])) , True , (0,0,0))), ((149+(i*273)),(280+(others*621))))
    pygame.display.flip()

def load_game(roads,settlements,cities,harbours,players, turnIndex):
    screen.fill((135, 206, 235))
    draw_harbours(harbours)
    create_game_screen()
    for road in roads:
        draw_road(road)
    for settlement in settlements:
        draw_settlement(settlement)
    for city in cities:
        draw_city(city)
    new_turn(turnIndex)
    draw_player_banners(players)

# ---------- INIT ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catan Board")

board = generate_catan_layout(WIDTH // 2, HEIGHT // 2)

# ---------- MAIN LOOP ----------
#test data#
roads = [(((5,2,3),(5,3,3)),'orange')]
settlements = [((2,2,0), 'blue')]
cities = [((3,5,-1),'red')]
harbours = [((0,0,0), 'any'), ((4,5,-1), 'ore')]
players = ['blue', 'red', 'orange', 'white']
turnIndex= 0
resources = []
devs =[]
#end of test data#
running = True
pressedNode = []
tradeOfferYou = []
tradeOfferOtherPlayers = []
acceptedTrade = []
playerToAsk = 0
currentScreen = 'game'
load_game(roads,settlements,cities,harbours,players,turnIndex)
update_longest_road(turnIndex)
update_largest_army(turnIndex)
while running:
    if len(pressedNode) == 2: # 2 being pressed causes building to occur
        time.sleep(0.15)
        print(pressedNode)
#!!!!!!!!!!!!BUILD!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for node in pressedNode: #make them appear unpressed
            pygame.draw.circle(screen, (135, 206, 235), node, 10)
            pygame.display.update(node[0]-10, node[1]-10, 20, 20)
        load_game(roads,settlements,cities, harbours,players,turnIndex)
        pressedNode = []
    for ev in pygame.event.get():   
        #checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if currentScreen == 'rules':
                if 1217 <= mouse[0] <= 1217+183 and 0 <= mouse[1] <= 0+75: #'back to game
                    currentScreen = 'game'
                    load_game(roads,settlements,cities, harbours,players,turnIndex)

            elif currentScreen == 'asking for trade': 
                if 460 <= mouse[0] <= 460+223.5 and 393 <= mouse[1] <= 393+414: #accept trade
                    acceptedTrade.append(playerToAsk)
                    playerToAsk += 1
                    if playerToAsk > 3 or (playerToAsk == 3 == turnIndex):
                        playerToAsk = 0
                        currentScreen = 'trade'
                        trade_screen()
                    else:
                        if playerToAsk == turnIndex:
                            playerToAsk +=1
                        askOtherPlayersForTrade(turnIndex,players,playerToAsk)
                elif 716.5 <= mouse[0] <= 716.5+223.5 and 393 <= mouse[1] <= 393+414: #decline trade
                    playerToAsk += 1
                    if playerToAsk > 3:
                        playerToAsk = 0
                        currentScreen = 'trade'
                        trade_screen()
                    else:
                        askOtherPlayersForTrade(turnIndex,players,playerToAsk)
            
            elif currentScreen == 'trade':
                if 1217 <= mouse[0] <= 1217+183 and 0 <= mouse[1] <= 0+75: #'cancel trade'
                    currentScreen = 'game'
                    tradeOfferYou.clear()
                    tradeOfferOtherPlayers.clear()
                    load_game(roads,settlements,cities, harbours, players, turnIndex)
                elif 0 <= mouse[0] <= 0+183 and 0 <= mouse[1] <= 0+75: # 'complete trade'
                    currentScreen = 'asking for trade'
                    if playerToAsk == turnIndex:
                        playerToAsk +=1
                    askOtherPlayersForTrade(turnIndex,players,playerToAsk)
                    print(tradeOfferYou)
                    print(tradeOfferOtherPlayers)
                #trade arrows - up arrows increase the number of that resourse involved in the trade by 1
                #down arrown decrease the number of that resource by 1 
                #you put in - the players whos turn it is 
                elif 41 <= mouse [0] <= 41 +75 and 252 <= mouse[1] <= 252 +75: # down
                    if 'wood' in tradeOfferYou:
                        tradeOfferYou.remove('wood')
                        reDrawTradeOfferYou(tradeOfferYou, False)
                elif 195 <= mouse [0] <= 195 +75 and 252 <= mouse[1] <= 252 +75: #up
                    tradeOfferYou.append('wood')
                    reDrawTradeOfferYou(tradeOfferYou, False)
                elif 314 <= mouse [0] <= 314 +75 and 252 <= mouse[1] <= 252 +75: # down
                    if 'brick' in tradeOfferYou:
                        tradeOfferYou.remove('brick')
                        reDrawTradeOfferYou(tradeOfferYou, False)
                elif 468 <= mouse [0] <= 468 +75 and 252 <= mouse[1] <= 252 +75: #up
                    tradeOfferYou.append('brick')
                    reDrawTradeOfferYou(tradeOfferYou, False)
                elif 587 <= mouse [0] <= 587 +75 and 252 <= mouse[1] <= 252 +75: # down
                    if 'sheep' in tradeOfferYou:
                        tradeOfferYou.remove('sheep')
                        reDrawTradeOfferYou(tradeOfferYou, False)
                elif 741 <= mouse [0] <= 741 +75 and 252 <= mouse[1] <= 252 +75: #up
                    tradeOfferYou.append('sheep')
                    reDrawTradeOfferYou(tradeOfferYou, False)
                elif 860 <= mouse [0] <= 860 +75 and 252 <= mouse[1] <= 252 +75: # down
                    if 'hay' in tradeOfferYou:
                        tradeOfferYou.remove('hay')
                        reDrawTradeOfferYou(tradeOfferYou, False)
                elif 1014 <= mouse [0] <= 1014 +75 and 252 <= mouse[1] <= 252 +75: #up
                    tradeOfferYou.append('hay')
                    reDrawTradeOfferYou(tradeOfferYou, False)
                elif 1133 <= mouse [0] <= 1133 +75 and 252 <= mouse[1] <= 252 +75: # down
                    if 'ore' in tradeOfferYou:
                        tradeOfferYou.remove('ore')
                        reDrawTradeOfferYou(tradeOfferYou, False)
                elif 1287 <= mouse [0] <= 1287 +75 and 252 <= mouse[1] <= 252 +75: #up
                    tradeOfferYou.append('ore')
                    reDrawTradeOfferYou(tradeOfferYou, False)
                #other players put in - what the player whos turn it is wants from other players 
                elif 41 <= mouse [0] <= 41 +75 and 873 <= mouse[1] <= 873 +75: # down
                    if 'wood' in tradeOfferOtherPlayers:
                        tradeOfferOtherPlayers.remove('wood')
                        reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
                elif 195 <= mouse [0] <= 195 +75 and 873 <= mouse[1] <= 873 +75: #up
                    tradeOfferOtherPlayers.append('wood')
                    reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
                elif 314 <= mouse [0] <= 314 +75 and 873 <= mouse[1] <= 873 +75: # down
                    if 'brick' in tradeOfferOtherPlayers:
                        tradeOfferOtherPlayers.remove('brick')
                        reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
                elif 468 <= mouse [0] <= 468 +75 and 873 <= mouse[1] <= 873 +75: #up
                    tradeOfferOtherPlayers.append('brick')
                    reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
                elif 587 <= mouse [0] <= 587 +75 and 873 <= mouse[1] <= 873 +75: # down
                    if 'sheep' in tradeOfferOtherPlayers:
                        tradeOfferOtherPlayers.remove('sheep')
                        reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
                elif 741 <= mouse [0] <= 741 +75 and 873 <= mouse[1] <= 873 +75: #up
                    tradeOfferOtherPlayers.append('sheep')
                    reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
                elif 860 <= mouse [0] <= 860 +75 and 873 <= mouse[1] <= 873 +75: # down
                    if 'hay' in tradeOfferOtherPlayers:
                        tradeOfferOtherPlayers.remove('hay')
                        reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
                elif 1014 <= mouse [0] <= 1014 +75 and 873 <= mouse[1] <= 873 +75: #up
                    tradeOfferOtherPlayers.append('hay')
                    reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
                elif 1133 <= mouse [0] <= 1133 +75 and 873 <= mouse[1] <= 873 +75: # down
                    if 'ore' in tradeOfferOtherPlayers:
                        tradeOfferOtherPlayers.remove('ore')
                        reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
                elif 1287 <= mouse [0] <= 1287 +75 and 873 <= mouse[1] <= 873 +75: #up
                    tradeOfferOtherPlayers.append('ore')
                    reDrawTradeOfferYou(tradeOfferOtherPlayers, True)
            
            else: # current screeen is game 
                if 1183 <= mouse[0] <= 1183+183 and 992 <= mouse[1] <= 992+75: # quit button
                    running = False
                elif 1183 <= mouse[0] <= 1183+183 and 884 <= mouse[1] <= 884+75: # roll dice button
                    print('roll dice')
                elif 34 <= mouse[0] <= 34+183 and 776 <= mouse[1] <= 776+75:#trade button
                    currentScreen = 'trade'
                    trade_screen()
                elif 34 <= mouse[0] <= 34+183 and 992 <= mouse[1] <= 992+75: #rules button
                    currentScreen = 'rules'
                    rules_screen()
                elif 34 <= mouse[0] <= 34+183 and 884 <= mouse[1] <= 884+75:
                    turnIndex += 1
                    if turnIndex > 3:
                        turnIndex = 0
                    new_turn(turnIndex)
                elif 34 <= mouse[0] <= 34+183 and 668 <= mouse[1] <= 668+75:
                    print('buy development card')
            # hex node buttons:
                elif  609.94 <= mouse[0] <= 629.94 and 275 <= mouse[1] <= 295 :
                    pygame.draw.circle(screen, (0,0,0), ( 619.94 , 285 ), 10,)
                    pygame.display.update( 609.94 , 275 , 629.94 , 295 )
                    pressedNode.append( (619.94 , 285) )
                elif  609.94 <= mouse[0] <= 629.94 and 365 <= mouse[1] <= 385 :
                    pygame.draw.circle(screen, (0,0,0), ( 619.94 , 375 ), 10,)
                    pygame.display.update( 609.94 , 365 , 629.94 , 385 )
                    pressedNode.append( (619.94 , 375) )
                elif  532 <= mouse[0] <= 552 and 410 <= mouse[1] <= 430 :
                    pygame.draw.circle(screen, (0,0,0), ( 542 , 420 ), 10,)
                    pygame.display.update( 532 , 410 , 552 , 430 )
                    pressedNode.append( (542 , 420) )
                elif  454.06 <= mouse[0] <= 474.06 and 365 <= mouse[1] <= 385 :
                    pygame.draw.circle(screen, (0,0,0), ( 464.06 , 375 ), 10,)
                    pygame.display.update( 454.06 , 365 , 474.06 , 385 )
                    pressedNode.append( (464.06 , 375 ))
                elif  454.06 <= mouse[0] <= 474.06 and 275 <= mouse[1] <= 295 :
                    pygame.draw.circle(screen, (0,0,0), ( 464.06 , 285 ), 10, )
                    pygame.display.update( 454.06 , 275 , 474.06 , 295 )
                    pressedNode.append( (464.06 , 285) )
                elif  532 <= mouse[0] <= 552 and 230 <= mouse[1] <= 250 :
                    pygame.draw.circle(screen, (0,0,0), ( 542 , 240 ), 10, )
                    pygame.display.update( 532 , 230 , 552 , 250 )
                    pressedNode.append( (542 , 240 ))
                elif  767.94 <= mouse[0] <= 787.94 and 275 <= mouse[1] <= 295 :
                    pygame.draw.circle(screen, (0,0,0), ( 777.94 , 285 ), 10, )
                    pygame.display.update( 767.94 , 275 , 787.94 , 295 )
                    pressedNode.append( (777.94 , 285 ))
                elif  767.94 <= mouse[0] <= 787.94 and 365 <= mouse[1] <= 385 :
                    pygame.draw.circle(screen, (0,0,0), ( 777.94 , 375 ), 10, )
                    pygame.display.update( 767.94 , 365 , 787.94 , 385 )
                    pressedNode.append( (777.94 , 375) )
                elif  690 <= mouse[0] <= 710 and 410 <= mouse[1] <= 430 :
                    pygame.draw.circle(screen, (0,0,0), ( 700 , 420 ), 10, )
                    pygame.display.update( 690 , 410 , 710 , 430 )
                    pressedNode.append(( 700 , 420) )
                elif  690 <= mouse[0] <= 710 and 230 <= mouse[1] <= 250 :
                    pygame.draw.circle(screen, (0,0,0), ( 700 , 240 ), 10, )
                    pygame.display.update( 690 , 230 , 710 , 250 )
                    pressedNode.append( (700 , 240) )
                elif  925.94 <= mouse[0] <= 945.94 and 275 <= mouse[1] <= 295 :
                    pygame.draw.circle(screen, (0,0,0), ( 935.94 , 285 ), 10, )
                    pygame.display.update( 925.94 , 275 , 945.94 , 295 )
                    pressedNode.append( (935.94 , 285 ))
                elif  925.94 <= mouse[0] <= 945.94 and 365 <= mouse[1] <= 385 :
                    pygame.draw.circle(screen, (0,0,0), ( 935.94 , 375 ), 10, )
                    pygame.display.update( 925.94 , 365 , 945.94 , 385 )
                    pressedNode.append( (935.94 , 375) )
                elif  848 <= mouse[0] <= 868 and 410 <= mouse[1] <= 430 :
                    pygame.draw.circle(screen, (0,0,0), ( 858 , 420 ), 10, )
                    pygame.display.update( 848 , 410 , 868 , 430 )
                    pressedNode.append( (858 , 420) )
                elif  848 <= mouse[0] <= 868 and 230 <= mouse[1] <= 250 :
                    pygame.draw.circle(screen, (0,0,0), ( 858 , 240 ), 10, )
                    pygame.display.update( 848 , 230 , 868 , 250 )
                    pressedNode.append( (858 , 240) )
                elif  531.94 <= mouse[0] <= 551.94 and 500 <= mouse[1] <= 520 :
                    pygame.draw.circle(screen, (0,0,0), ( 541.94 , 510 ), 10, )
                    pygame.display.update( 531.94 , 500 , 551.94 , 520 )
                    pressedNode.append( (541.94 , 510) )
                elif  454 <= mouse[0] <= 474 and 545 <= mouse[1] <= 565 :
                    pygame.draw.circle(screen, (0,0,0), ( 464 , 555 ), 10, )
                    pygame.display.update( 454 , 545 , 474 , 565 )
                    pressedNode.append( (464 , 555) )
                elif  376.06 <= mouse[0] <= 396.06 and 500 <= mouse[1] <= 520 :
                    pygame.draw.circle(screen, (0,0,0), ( 386.06 , 510 ), 10, )
                    pygame.display.update( 376.06 , 500 , 396.06 , 520 )
                    pressedNode.append( (386.06 , 510) )
                elif  376.06 <= mouse[0] <= 396.06 and 410 <= mouse[1] <= 430 :
                    pygame.draw.circle(screen, (0,0,0), ( 386.06 , 420 ), 10, )
                    pygame.display.update( 376.06 , 410 , 396.06 , 430 )
                    pressedNode.append( (386.06 , 420) )
                elif  689.94 <= mouse[0] <= 709.94 and 500 <= mouse[1] <= 520 :
                    pygame.draw.circle(screen, (0,0,0), ( 699.94 , 510 ), 10, )
                    pygame.display.update( 689.94 , 500 , 709.94 , 520 )
                    pressedNode.append( (699.94 , 510) )
                elif  612 <= mouse[0] <= 632 and 545 <= mouse[1] <= 565 :
                    pygame.draw.circle(screen, (0,0,0), ( 622 , 555 ), 10, )
                    pygame.display.update( 612 , 545 , 632 , 565 )
                    pressedNode.append( (622 , 555) )
                elif  847.94 <= mouse[0] <= 867.94 and 500 <= mouse[1] <= 520 :
                    pygame.draw.circle(screen, (0,0,0), ( 857.94 , 510 ), 10, )
                    pygame.display.update( 847.94 , 500 , 867.94 , 520 )
                    pressedNode.append( (857.94 , 510) )
                elif  770 <= mouse[0] <= 790 and 545 <= mouse[1] <= 565 :
                    pygame.draw.circle(screen, (0,0,0), ( 780 , 555 ), 10, )
                    pygame.display.update( 770 , 545 , 790 , 565 )
                    pressedNode.append( (780 , 555) )
                elif  1005.94 <= mouse[0] <= 1025.94 and 410 <= mouse[1] <= 430 :
                    pygame.draw.circle(screen, (0,0,0), ( 1015.94 , 420 ), 10, )
                    pygame.display.update( 1005.94 , 410 , 1025.94 , 430 )
                    pressedNode.append( (1015.94 , 420) )
                elif  1005.94 <= mouse[0] <= 1025.94 and 500 <= mouse[1] <= 520 :
                    pygame.draw.circle(screen, (0,0,0), ( 1015.94 , 510 ), 10, )
                    pygame.display.update( 1005.94 , 500 , 1025.94 , 520 )
                    pressedNode.append( (1015.94 , 510) )
                elif  928 <= mouse[0] <= 948 and 545 <= mouse[1] <= 565 :
                    pygame.draw.circle(screen, (0,0,0), ( 938 , 555 ), 10, )
                    pygame.display.update( 928 , 545 , 948 , 565 )
                    pressedNode.append( (938 , 555) )
                elif  452.94 <= mouse[0] <= 472.94 and 635 <= mouse[1] <= 655 :
                    pygame.draw.circle(screen, (0,0,0), ( 462.94 , 645 ), 10, )
                    pygame.display.update( 452.94 , 635 , 472.94 , 655 )
                    pressedNode.append( (462.94 , 645) )
                elif  375 <= mouse[0] <= 395 and 680 <= mouse[1] <= 700 :
                    pygame.draw.circle(screen, (0,0,0), ( 385 , 690 ), 10, )
                    pygame.display.update( 375 , 680 , 395 , 700 )
                    pressedNode.append( (385 , 690) )
                elif  297.06 <= mouse[0] <= 317.06 and 635 <= mouse[1] <= 655 :
                    pygame.draw.circle(screen, (0,0,0), ( 307.06 , 645 ), 10, )
                    pygame.display.update( 297.06 , 635 , 317.06 , 655 )
                    pressedNode.append( (307.06 , 645) )
                elif  297.06 <= mouse[0] <= 317.06 and 545 <= mouse[1] <= 565 :
                    pygame.draw.circle(screen, (0,0,0), ( 307.06 , 555 ), 10, )
                    pygame.display.update( 297.06 , 545 , 317.06 , 565 )
                    pressedNode.append( (307.06 , 555) )
                elif  610.94 <= mouse[0] <= 630.94 and 635 <= mouse[1] <= 655 :
                    pygame.draw.circle(screen, (0,0,0), ( 620.94 , 645 ), 10, )
                    pygame.display.update( 610.94 , 635 , 630.94 , 655 )
                    pressedNode.append( (620.94 , 645) )
                elif  533 <= mouse[0] <= 553 and 680 <= mouse[1] <= 700 :
                    pygame.draw.circle(screen, (0,0,0), ( 543 , 690 ), 10, )
                    pygame.display.update( 533 , 680 , 553 , 700 )
                    pressedNode.append( (543 , 690) )
                elif  768.94 <= mouse[0] <= 788.94 and 635 <= mouse[1] <= 655 :
                    pygame.draw.circle(screen, (0,0,0), ( 778.94 , 645 ), 10, )
                    pygame.display.update( 768.94 , 635 , 788.94 , 655 )
                    pressedNode.append( (778.94 , 645) )
                elif  691 <= mouse[0] <= 711 and 680 <= mouse[1] <= 700 :
                    pygame.draw.circle(screen, (0,0,0), ( 701 , 690 ), 10, )
                    pygame.display.update( 691 , 680 , 711 , 700 )
                    pressedNode.append( (701 , 690) )
                elif  926.94 <= mouse[0] <= 946.94 and 635 <= mouse[1] <= 655 :
                    pygame.draw.circle(screen, (0,0,0), ( 936.94 , 645 ), 10, )
                    pygame.display.update( 926.94 , 635 , 946.94 , 655 )
                    pressedNode.append( (936.94 , 645) )
                elif  849 <= mouse[0] <= 869 and 680 <= mouse[1] <= 700 :
                    pygame.draw.circle(screen, (0,0,0), ( 859 , 690 ), 10, )
                    pygame.display.update( 849 , 680 , 869 , 700 )
                    pressedNode.append( (859 , 690) )
                elif  1084.94 <= mouse[0] <= 1104.94 and 545 <= mouse[1] <= 565 :
                    pygame.draw.circle(screen, (0,0,0), ( 1094.94 , 555 ), 10, )
                    pygame.display.update( 1084.94 , 545 , 1104.94 , 565 )
                    pressedNode.append( (1094.94 , 555) )
                elif  1084.94 <= mouse[0] <= 1104.94 and 635 <= mouse[1] <= 655 :
                    pygame.draw.circle(screen, (0,0,0), ( 1094.94 , 645 ), 10, )
                    pygame.display.update( 1084.94 , 635 , 1104.94 , 655 )
                    pressedNode.append( (1094.94 , 645 ))
                elif  1007 <= mouse[0] <= 1027 and 680 <= mouse[1] <= 700 :
                    pygame.draw.circle(screen, (0,0,0), ( 1017 , 690 ), 10, )
                    pygame.display.update( 1007 , 680 , 1027 , 700 )
                    pressedNode.append( (1017 , 690) )
                elif  531.94 <= mouse[0] <= 551.94 and 770 <= mouse[1] <= 790 :
                    pygame.draw.circle(screen, (0,0,0), ( 541.94 , 780 ), 10, )
                    pygame.display.update( 531.94 , 770 , 551.94 , 790 )
                    pressedNode.append( (541.94 , 780) )
                elif  454 <= mouse[0] <= 474 and 815 <= mouse[1] <= 835 :
                    pygame.draw.circle(screen, (0,0,0), ( 464 , 825 ), 10, )
                    pygame.display.update( 454 , 815 , 474 , 835 )
                    pressedNode.append( (464 , 825) )
                elif  376.06 <= mouse[0] <= 396.06 and 770 <= mouse[1] <= 790 :
                    pygame.draw.circle(screen, (0,0,0), ( 386.06 , 780 ), 10, )
                    pygame.display.update( 376.06 , 770 , 396.06 , 790 )
                    pressedNode.append( (386.06 , 780) )
                elif  689.94 <= mouse[0] <= 709.94 and 770 <= mouse[1] <= 790 :
                    pygame.draw.circle(screen, (0,0,0), ( 699.94 , 780 ), 10, )
                    pygame.display.update( 689.94 , 770 , 709.94 , 790 )
                    pressedNode.append( (699.94 , 780) )
                elif  612 <= mouse[0] <= 632 and 815 <= mouse[1] <= 835 :
                    pygame.draw.circle(screen, (0,0,0), ( 622 , 825 ), 10, )
                    pygame.display.update( 612 , 815 , 632 , 835 )
                    pressedNode.append( (622 , 825 ))
                elif  847.94 <= mouse[0] <= 867.94 and 770 <= mouse[1] <= 790 :
                    pygame.draw.circle(screen, (0,0,0), ( 857.94 , 780 ), 10, )
                    pygame.display.update( 847.94 , 770 , 867.94 , 790 )
                    pressedNode.append( (857.94 , 780) )
                elif  770 <= mouse[0] <= 790 and 815 <= mouse[1] <= 835 :
                    pygame.draw.circle(screen, (0,0,0), ( 780 , 825 ), 10, )
                    pygame.display.update( 770 , 815 , 790 , 835 )
                    pressedNode.append( (780 , 825) )
                elif  1005.94 <= mouse[0] <= 1025.94 and 770 <= mouse[1] <= 790 :
                    pygame.draw.circle(screen, (0,0,0), ( 1015.94 , 780 ), 10, )
                    pygame.display.update( 1005.94 , 770 , 1025.94 , 790 )
                    pressedNode.append( (1015.94 , 780) )
                elif  928 <= mouse[0] <= 948 and 815 <= mouse[1] <= 835 :
                    pygame.draw.circle(screen, (0,0,0), ( 938 , 825 ), 10, )
                    pygame.display.update( 928 , 815 , 948 , 835 )
                    pressedNode.append( (938 , 825) )
                elif  609.94 <= mouse[0] <= 629.94 and 905 <= mouse[1] <= 925 :
                    pygame.draw.circle(screen, (0,0,0), ( 619.94 , 915 ), 10, )
                    pygame.display.update( 609.94 , 905 , 629.94 , 925 )
                    pressedNode.append( (619.94 , 915) )
                elif  532 <= mouse[0] <= 552 and 950 <= mouse[1] <= 970 :
                    pygame.draw.circle(screen, (0,0,0), ( 542 , 960 ), 10, )
                    pygame.display.update( 532 , 950 , 552 , 970 )
                    pressedNode.append( (542 , 960) )
                elif  454.06 <= mouse[0] <= 474.06 and 905 <= mouse[1] <= 925 :
                    pygame.draw.circle(screen, (0,0,0), ( 464.06 , 915 ), 10, )
                    pygame.display.update( 454.06 , 905 , 474.06 , 925 )
                    pressedNode.append( (464.06 , 915) )
                elif  767.94 <= mouse[0] <= 787.94 and 905 <= mouse[1] <= 925 :
                    pygame.draw.circle(screen, (0,0,0), ( 777.94 , 915 ), 10, )
                    pygame.display.update( 767.94 , 905 , 787.94 , 925 )
                    pressedNode.append( (777.94 , 915) )
                elif  690 <= mouse[0] <= 710 and 950 <= mouse[1] <= 970 :
                    pygame.draw.circle(screen, (0,0,0), ( 700 , 960 ), 10, )
                    pygame.display.update( 690 , 950 , 710 , 970 )
                    pressedNode.append( (700 , 960) )
                elif  925.94 <= mouse[0] <= 945.94 and 905 <= mouse[1] <= 925 :
                    pygame.draw.circle(screen, (0,0,0), ( 935.94 , 915 ), 10, )
                    pygame.display.update( 925.94 , 905 , 945.94 , 925 )
                    pressedNode.append( (935.94 , 915) )
                elif  848 <= mouse[0] <= 868 and 950 <= mouse[1] <= 970 :
                    pygame.draw.circle(screen, (0,0,0), ( 858 , 960 ), 10, )
                    pygame.display.update( 848 , 950 , 868 , 970 )
                    pressedNode.append( (858 , 960) )
                
pygame.quit()