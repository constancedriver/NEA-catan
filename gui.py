import pygame
import math
import time
import sys
pygame.font.init()

WIDTH, HEIGHT = 1400, 1200
SMALLFONT = pygame.font.SysFont('Corbel',35)
HEX_RADIUS = 90
PLAYER_COLOURS = ['white', 'blue', 'red', 'orange']

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
    'white':(255,255,255),
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

def draw_hex(surface, color, center, radius=HEX_RADIUS):
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, (0, 0, 0), points, 3)  

def generate_catan_layout(center_x, center_y, hexRadius=HEX_RADIUS): # add tiles as parameter
    colours = get_resource_colours() # add tiles as parameter
    layout = []
    rows = [3, 4, 5, 4, 3]
    h_spacing = hexRadius * 1.75
    v_spacing = hexRadius * 1.5

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

def display_dice(dice1, dice2):
    pygame.draw.rect(screen, (255,255,255), (1183, 884, 75, 75))
    pygame.draw.rect(screen, (255,255,255), (1291, 884, 75, 75))
    screen.blit((SMALLFONT.render(str(dice1) , True , (0,0,0))), (1214,909))
    screen.blit((SMALLFONT.render(str(dice2) , True , (0,0,0))), (1322,909))
    pygame.display.update(1183, 884, 183, 75)

def create_hex_node_buttons():
    hex_node_coordinates = [(619.94,285),(619.94,375),(542,420),(464.06,375),(464.06,285),(542,240),(777.94,285),(777.94,375),(700,420),(700,240),(935.94,285),(935.94,375),(858,420),(858,240),(541.94,510),(464,555),(386.06,510),(386.06,420),(699.94,510),(622,555),(857.94,510),(780,555),(1015.94,420),(1015.94,510),(938,555),(462.94,645),(385,690),(307.06,645), (307.06,555),(620.94,645), (543,690),(778.94,645), (701,690),(936.94,645), (859,690),(1094.94,555), (1094.94,645),(1017,690),(541.94,780),(464,825), (386.06,780),(699.94,780), (622,825),(857.94,780), (780,825),(1015.94,780),(938,825), (619.94,915),(542,960),(464.06,915),(777.94,915),(700,960),(935.94,915), (858,960)]
    for node in hex_node_coordinates:
        pygame.draw.circle(screen, (0,0,0), node, 10, 2)

def draw_player_banners(players):
    pygame.draw.rect(screen, get_colour(players[0]), (1183, 20, 183, 193))
    pygame.draw.rect(screen, get_colour(players[1]), (1183, 233, 183, 193))
    pygame.draw.rect(screen, get_colour(players[2]), (1183, 446, 183, 193))
    pygame.draw.rect(screen, get_colour(players[3]), (1183, 659, 183, 193))
    for i in range (0,4,1):
        screen.blit((SMALLFONT.render(('VPs:') , True , (0,0,0))), (1188,30+(i*213)))
        screen.blit((SMALLFONT.render(('resources:') , True , (0,0,0))), (1188,70+(i*213)))
        screen.blit((SMALLFONT.render(('devs:') , True , (0,0,0))), (1188,110+(i*213)))
        screen.blit((SMALLFONT.render(('knights:') , True , (0,0,0))), (1188,150+(i*213)))
    pygame.display.update(1183, 20, 183, 1150)

def update_banner_resources(listOfPlayerResources:list):
    for i in range(0,4,1):
        pygame.draw.rect(screen, get_colour(players[i]), (1315,70+(i*213), 50, 20))
        screen.blit((SMALLFONT.render(str(len(listOfPlayerResources[i])) , True , (0,0,0))), (1318,70+(i*213)))
    pygame.display.update(1315, 20, 50, 1150)

def update_vp(turnIndex, vp):
    pygame.draw.rect(screen, get_colour(players[turnIndex]), (1315,30+(turnIndex*213), 50, 20))
    screen.blit((SMALLFONT.render(str(vp) , True , (0,0,0))), (1318,30+(turnIndex*213)))
    pygame.display.update(1315, 30+(turnIndex*213), 50, 20)

def update_devs(turnIndex, devs):
    pygame.draw.rect(screen, get_colour(players[turnIndex]), (1315,110+(turnIndex*213), 50, 20))
    screen.blit((SMALLFONT.render(str(devs) , True , (0,0,0))), (1318,110+(turnIndex*213)))
    pygame.display.update(1315, 110+(turnIndex*213), 50, 20)

def update_knights(turnIndex, knights):
    pygame.draw.rect(screen, get_colour(players[turnIndex]), (1315,150+(turnIndex*213), 50, 20))
    screen.blit((SMALLFONT.render(str(knights) , True , (0,0,0))), (1318,150+(turnIndex*213)))
    pygame.display.update(1315, 150+(turnIndex*213), 50, 20)

def move_robber(hex):
    resNum = ['5','6','11','8','3','4','5','9','11','','3','8','12','6','4','10','10','2','9']
    i = 0
    for hex_center, colour in board:
        draw_center_circle(screen, hex_center, CIRCLE_RADIUS)
        screen.blit((SMALLFONT.render(str(resNum[i]) , True , (0,0,0))), (hex_center[0]-8,hex_center[1]-10))
        i += 1
    hex_bottom_coord = convert_coordinates(hex)
    pygame.draw.circle(screen, (100,100,100), (hex_bottom_coord[0], hex_bottom_coord[1]-105), 15)
    pygame.draw.rect(screen, (100,100,100), (hex_bottom_coord[0]-10, hex_bottom_coord[1]-95,20,30))
    pygame.display.flip()       

def update_longest_road(player):
    colour = players[player]
    pygame.draw.rect(screen, get_colour(colour), (34,510,149,30))
    pygame.display.update(34,510,149,30)

def update_largest_army(player):
    colour = players[player]
    pygame.draw.rect(screen, get_colour(colour), (34,580,149,30))
    pygame.display.update(34,580,149,30)

def new_turn(playerColours=PLAYER_COLOURS): # !!!!!!!!!!!!!!!! INPUT PLAYER HAND PROPERTIES!!!!!!!!!!!!!
    player = game1.players[game1.turnIndex]
    colour = playerColours[game1.turnIndex]
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
    screen.blit((SMALLFONT.render(('roads left:'+str(player.roadsLeft)) , True , (0,0,0))), (316,130))
    screen.blit((SMALLFONT.render(('settlements left:'+str(player.settlementsLeft)) , True , (0,0,0))), (716,130))
    screen.blit((SMALLFONT.render(('cities left:'+str(player.citiesLeft)) , True , (0,0,0))), (316,160))
    screen.blit((SMALLFONT.render(('knights played:'+str(player.knightsPlayed)) , True , (0,0,0))), (716,160))
    screen.blit((SMALLFONT.render(('dev:') , True , (0,0,0))), (316,80))
    i = 1
    for card in player.development:
        screen.blit((SMALLFONT.render((card) , True , (0,0,0))), (316+100*i,80))
        i+=1
    pygame.display.update(283,1000, 834, 100)
    pygame.display.update(283,0, 834, 200)

def node_pressed(node):
    pygame.draw.circle(screen, (0,0,0), (node[0] ,node[1]), 10, )
    pygame.display.update( 848 , 950 , 868 , 970 )

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
    screen.fill((135, 206, 235))
    resNum = ['5','6','11','8','3','4','5','9','11','','3','8','12','6','4','10','10','2','9']
    i = 0
    for hex_center, colour in board:
        draw_hex(screen, colour, hex_center)
        pygame.draw.circle(screen, (204, 173, 96), hex_center, 35)
        screen.blit((SMALLFONT.render(str(resNum[i]) , True , (0,0,0))), (hex_center[0]-8,hex_center[1]-10))
        i += 1
    pygame.draw.rect(screen, (204, 173, 96), (0,0, 250, 1200))
    pygame.draw.rect(screen, (204, 173, 96), (1150,0, 250, 1200))
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
    pygame.display.flip()

def rules_screen():
    screen.fill((204, 173, 96))
    pygame.draw.rect(screen, (255,0,0), (1217, 0, 183, 75))
    screen.blit((SMALLFONT.render('back to game' , True , (0,0,0))), (1233,25))
    pygame.display.flip()
 #!!!!!###### print actual rules!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def game_end_screen(turnIndex,playerColours=PLAYER_COLOURS):
    colour = playerColours[turnIndex]
    screen.fill((get_colour(colour)))
    screen.blit((SMALLFONT.render('GAME END' , True , (0,0,0))), (620,550))
    pygame.draw.rect(screen, (255,0,0), (1183, 992, 183, 75))
    screen.blit((SMALLFONT.render('quit' , True , (0,0,0))), (1249,1017))
    pygame.display.flip()

def trade_screen():
    screen.fill((204, 173, 96))
    pygame.draw.rect(screen, (255,0,0), (1217, 0, 183, 75))
    screen.blit((SMALLFONT.render('cancel trade' , True , (0,0,0))), (1233,25))
    pygame.draw.rect(screen, (0,255,0), (0, 0, 183, 75))
    screen.blit((SMALLFONT.render('complete trade' , True , (0,0,0))), (6,25))
    screen.blit((SMALLFONT.render('TRADE MENU' , True , (0,0,0))), (620,25))
    pygame.draw.rect(screen, (255,255,255), (34, 992, 183, 75))
    screen.blit((SMALLFONT.render('rules' , True , (0,0,0))), (95,1017))
    #creating cards
    pygame.draw.rect(screen, (get_colour('wood')), (34, 360, 240, 480))
    pygame.draw.rect(screen, (get_colour('brick')), (307, 360, 240, 480))
    pygame.draw.rect(screen, (get_colour('sheep')), (580, 360, 240, 480))
    pygame.draw.rect(screen, (get_colour('hay')), (853, 360, 240, 480))
    pygame.draw.rect(screen, (get_colour('ore')), (1126, 360, 240, 480))
    # creating arrows
    screen.blit((SMALLFONT.render('You put in:' , True , (0,0,0))), (300,150))
    screen.blit((SMALLFONT.render('Other players put in:' , True , (0,0,0))), (300,1000))
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

def update_year_of_plenty(resources:list):
    if len(resources) <= 2:
        pygame.draw.rect(screen, get_colour('wood'), (409, 714, 36,36))
        pygame.draw.rect(screen, (0,0,0), (409, 714, 36,36), 2)
        screen.blit((SMALLFONT.render(str(resources.count('wood')) , True , (0,0,0))), (419,724))

        pygame.draw.rect(screen, get_colour('brick'), (409, 755, 36,36))
        pygame.draw.rect(screen, (0,0,0), (409, 755, 36,36), 2)
        screen.blit((SMALLFONT.render(str(resources.count('brick')) , True , (0,0,0))), (419,765))

        pygame.draw.rect(screen, get_colour('sheep'), (409, 796, 36,36))
        pygame.draw.rect(screen, (0,0,0), (409, 796, 36,36), 2)
        screen.blit((SMALLFONT.render(str(resources.count('sheep')) , True , (0,0,0))), (419,806))

        pygame.draw.rect(screen, get_colour('hay'), (409, 837, 36,36))
        pygame.draw.rect(screen, (0,0,0), (409, 837, 36,36), 2)
        screen.blit((SMALLFONT.render(str(resources.count('hay')) , True , (0,0,0))), (419,847))

        pygame.draw.rect(screen, get_colour('ore'), (409, 878, 36,36))
        pygame.draw.rect(screen, (0,0,0), (409, 878, 36,36), 2)
        screen.blit((SMALLFONT.render(str(resources.count('ore')) , True , (0,0,0))), (419,888))

def development_screen():
    screen.fill((204, 173, 96))
    screen.blit((SMALLFONT.render('DEVELOPMENT CARDS' , True , (0,0,0))), (620,25))
    screen.blit((SMALLFONT.render('Play:' , True , (0,0,0))), (100,300))

    pygame.draw.rect(screen, (get_colour('sheep')), (307, 360, 240, 75))
    screen.blit((SMALLFONT.render('knight' , True , (0,0,0))), (310,370))

    pygame.draw.rect(screen, (get_colour('brick')), (307, 468, 240, 75))
    screen.blit((SMALLFONT.render('road building' , True , (0,0,0))), (310,478))

    pygame.draw.rect(screen, (get_colour('wood')), (307, 576, 240, 75))
    screen.blit((SMALLFONT.render('monopoly' , True , (0,0,0))), (310,586))
    pygame.draw.rect(screen, get_colour('wood'), (310, 610, 36,36))
    pygame.draw.rect(screen, (0,0,0), (310, 610, 36,36), 2)
    pygame.draw.rect(screen, get_colour('brick'), (351, 610, 36,36))
    pygame.draw.rect(screen, (0,0,0), (351, 610, 36,36), 2)
    pygame.draw.rect(screen, get_colour('sheep'), (392, 610, 36,36))
    pygame.draw.rect(screen, (0,0,0), (392, 610, 36,36), 2)
    pygame.draw.rect(screen, get_colour('hay'), (433, 610, 36,36))
    pygame.draw.rect(screen, (0,0,0), (433, 610, 36,36), 2)
    pygame.draw.rect(screen, get_colour('ore'), (472, 610, 36,36))
    pygame.draw.rect(screen, (0,0,0), (472, 610, 36,36), 2)

    pygame.draw.rect(screen, (get_colour('hay')), (307, 684, 240, 240))
    screen.blit((SMALLFONT.render('year of plenty' , True , (0,0,0))), (310,694))
    for i in range (0,5,1):
        pygame.draw.polygon(screen, (0,0,0), ((450,(719+i*41)), (450,(745+i*41)), (476,(732+i*41))))# up
        pygame.draw.polygon(screen, (0,0,0), ((404,(719+i*41)), (404,(745+i*41)), (378,(732+i*41))))
    update_year_of_plenty([])

    pygame.draw.rect(screen, (get_colour('any')), (853, 360, 240, 480))
    screen.blit((SMALLFONT.render('Buy' , True , (0,0,0))), (860,370))

    pygame.draw.rect(screen, (255,255,255), (34, 992, 183, 75))
    screen.blit((SMALLFONT.render('rules' , True , (0,0,0))), (95,1017))
    pygame.draw.rect(screen, (255,0,0), (1217, 0, 183, 75))
    screen.blit((SMALLFONT.render('back to game' , True , (0,0,0))), (1233,25))
    pygame.display.flip()

def select_knight_placement_screen(): # create buttons for this
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (204, 173, 96), (0,0, 250, 1200))
    pygame.draw.rect(screen, (204, 173, 96), (1150,0, 250, 1200))
    pygame.draw.rect(screen, (255,0,0), (1183, 992, 183, 75))
    screen.blit((SMALLFONT.render('quit' , True , (0,0,0))), (1249,1017))
    resNum = ['5','6','11','8','3','4','5','9','11','','3','8','12','6','4','10','10','2','9']
    i = 0
    for hex_center, colour in board:
        draw_hex(screen, colour, hex_center)
        pygame.draw.circle(screen, (145, 105, 2), hex_center, 35)
        screen.blit((SMALLFONT.render(str(resNum[i]) , True , (0,0,0))), (hex_center[0]-8,hex_center[1]-10))
        i += 1
    pygame.display.flip()
    
    #giving inputs to game file

def command(currentScreen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #rule screen
                if 1217 <= mouse[0] <= 1217+183 and 0 <= mouse[1] <= 0+75: #back to game
                        message = 'exit rules'

                # all screens 
                elif 1183 <= mouse[0] <= 1183+183 and 992 <= mouse[1] <= 992+75: # quit button
                        pygame.quit()
                        sys.exit()
                elif 34 <= mouse[0] <= 34+183 and 992 <= mouse[1] <= 992+75: #rules button
                        message = 'rules'

                #trade screen 
                if currentScreen == 'ask player about trade':
                    if 460 <= mouse[0] <= 460+223.5 and 393 <= mouse[1] <= 393+414: #accept trade
                            message = 'accept trade'
                    elif 716.5 <= mouse[0] <= 716.5+223.5 and 393 <= mouse[1] <= 393+414: #decline trade
                            message = 'decline trade'
                
                elif currentScreen == 'trade':
                    if 1217 <= mouse[0] <= 1217+183 and 0 <= mouse[1] <= 0+75: #'cancel trade'
                        message = 'cancel trade'
                    elif 0 <= mouse[0] <= 0+183 and 0 <= mouse[1] <= 0+75: # 'complete trade'
                        message = 'complete trade'

                    #trade arrows - up arrows increase the number of that resourse involved in the trade by 1
                    #down arrown decrease the number of that resource by 1 
                    #you put in - the players whos turn it is 
                    elif 41 <= mouse [0] <= 41 +75 and 252 <= mouse[1] <= 252 +75: # down
                        message = 'turn player: remove wood'
                    elif 195 <= mouse [0] <= 195 +75 and 252 <= mouse[1] <= 252 +75: #up
                        message = 'turn player: add wood'
                    elif 314 <= mouse [0] <= 314 +75 and 252 <= mouse[1] <= 252 +75: # down
                        message = 'turn player: remove brick'
                    elif 468 <= mouse [0] <= 468 +75 and 252 <= mouse[1] <= 252 +75: #up
                        message = 'turn player: add brick'
                    elif 587 <= mouse [0] <= 587 +75 and 252 <= mouse[1] <= 252 +75: # down
                        message = 'turn player: remove sheep'
                    elif 741 <= mouse [0] <= 741 +75 and 252 <= mouse[1] <= 252 +75: #up
                        message = 'turn player: add sheep'
                    elif 860 <= mouse [0] <= 860 +75 and 252 <= mouse[1] <= 252 +75: # down
                        message = 'turn player: remove hay'
                    elif 1014 <= mouse [0] <= 1014 +75 and 252 <= mouse[1] <= 252 +75: #up
                        message = 'turn player: add hay'
                    elif 1133 <= mouse [0] <= 1133 +75 and 252 <= mouse[1] <= 252 +75: # down
                        message = 'turn player: remove ore'
                    elif 1287 <= mouse [0] <= 1287 +75 and 252 <= mouse[1] <= 252 +75: #up
                        message = 'turn player: add ore'

                    #other players put in - what the player whos turn it is wants from other players 
                    elif 41 <= mouse [0] <= 41 +75 and 873 <= mouse[1] <= 873 +75: # down
                        message = 'other players: remove wood'
                    elif 195 <= mouse [0] <= 195 +75 and 873 <= mouse[1] <= 873 +75: #up
                        message = 'other players: add wood'
                    elif 314 <= mouse [0] <= 314 +75 and 873 <= mouse[1] <= 873 +75: # down
                        message = 'other players: remove brick'
                    elif 468 <= mouse [0] <= 468 +75 and 873 <= mouse[1] <= 873 +75: #up
                        message = 'other players: add brick'
                    elif 587 <= mouse [0] <= 587 +75 and 873 <= mouse[1] <= 873 +75: # down
                        message = 'other players: remove sheep'
                    elif 741 <= mouse [0] <= 741 +75 and 873 <= mouse[1] <= 873 +75: #up
                        message = 'other players: add sheep'
                    elif 860 <= mouse [0] <= 860 +75 and 873 <= mouse[1] <= 873 +75: # down
                        message = 'other players: remove hay'
                    elif 1014 <= mouse [0] <= 1014 +75 and 873 <= mouse[1] <= 873 +75: #up
                        message = 'other players: add hay'
                    elif 1133 <= mouse [0] <= 1133 +75 and 873 <= mouse[1] <= 873 +75: # down
                        message = 'other players: remove ore'
                    elif 1287 <= mouse [0] <= 1287 +75 and 873 <= mouse[1] <= 873 +75: #up
                        message = 'other players: add ore'
                
                elif currentScreen == 'development':
                    if 307 <= mouse[0] <= 307+240 and 360 <= mouse[1] <= 360+75:
                        message = 'play knight'
                    elif 307 <= mouse[0] <= 307+240 and 468 <= mouse[1] <= 468+75:
                        message = 'play road building'
                    elif 310 <= mouse[0] <= 310+36 and 610 <= mouse[1] <= 610+36:
                        message = 'play monopoly wood'
                    elif 351 <= mouse[0] <= 351+36 and 610 <= mouse[1] <= 610+36:
                        message = 'play monopoly brick'
                    elif 392 <= mouse[0] <= 392+36 and 610 <= mouse[1] <= 610+36:
                        message = 'play monopoly sheep'
                    elif 433 <= mouse[0] <= 433+36 and 610 <= mouse[1] <= 610+36:
                        message = 'play monopoly hay'
                    elif 472 <= mouse[0] <= 472+36 and 610 <= mouse[1] <= 610+36:
                        message = 'play monopoly ore'
                    elif 307 <= mouse[0] <= 307+240 and 684 <= mouse[1] <= 684+75:
                        message = 'play year of plenty complete'
                    elif 853 <= mouse[0] <= 853+240 and 360 <= mouse[1] <= 360+480:
                        message = 'buy development'
                    elif 853 <= mouse[0] <= 853+240 and 360 <= mouse[1] <= 360+480:
                        message = 'load game screen'

                elif currentScreen == 'game':
                        if 1183 <= mouse[0] <= 1183+183 and 884 <= mouse[1] <= 884+75: # roll dice button
                            message = 'roll dice'
                        elif 34 <= mouse[0] <= 34+183 and 776 <= mouse[1] <= 776+75:#trade button
                            message = 'trade'
                        elif 34 <= mouse[0] <= 34+183 and 668 <= mouse[1] <= 668+75: # end turn
                            message = 'development'
                        elif 34 <= mouse[0] <= 34+183 and 884 <= mouse[1] <= 884+75: # end turn
                            message = 'end turn'
                        
                    # hex node buttons:
                        elif  609.94 <= mouse[0] <= 629.94 and 275 <= mouse[1] <= 295 :
                            message = (619.94 , 285)
                        elif  609.94 <= mouse[0] <= 629.94 and 365 <= mouse[1] <= 385 :
                            message = (619.94 , 375) 
                        elif  532 <= mouse[0] <= 552 and 410 <= mouse[1] <= 430 :
                            message = (542 , 420)
                        elif  454.06 <= mouse[0] <= 474.06 and 365 <= mouse[1] <= 385 :
                            message = (464.06 , 375 )
                        elif  454.06 <= mouse[0] <= 474.06 and 275 <= mouse[1] <= 295 :
                            message = (464.06 , 285)
                        elif  532 <= mouse[0] <= 552 and 230 <= mouse[1] <= 250 :
                            message = (542 , 240 )
                        elif  767.94 <= mouse[0] <= 787.94 and 275 <= mouse[1] <= 295 :
                            message = (777.94 , 285 )
                        elif  767.94 <= mouse[0] <= 787.94 and 365 <= mouse[1] <= 385 :
                            message = (777.94 , 375)
                        elif  690 <= mouse[0] <= 710 and 410 <= mouse[1] <= 430 :
                            message = ( 700 , 420) 
                        elif  690 <= mouse[0] <= 710 and 230 <= mouse[1] <= 250 :
                            message = (700 , 240)
                        elif  925.94 <= mouse[0] <= 945.94 and 275 <= mouse[1] <= 295 :
                            message = (935.94 , 285 )
                        elif  925.94 <= mouse[0] <= 945.94 and 365 <= mouse[1] <= 385 :
                            message = (935.94 , 375)
                        elif  848 <= mouse[0] <= 868 and 410 <= mouse[1] <= 430 :
                            message = (858 , 420) 
                        elif  848 <= mouse[0] <= 868 and 230 <= mouse[1] <= 250 :
                            message = (858 , 240)
                        elif  531.94 <= mouse[0] <= 551.94 and 500 <= mouse[1] <= 520 :
                            message = (541.94 , 510) 
                        elif  454 <= mouse[0] <= 474 and 545 <= mouse[1] <= 565 :
                            message = (464 , 555)
                        elif  376.06 <= mouse[0] <= 396.06 and 500 <= mouse[1] <= 520 :
                            message = (386.06 , 510)
                        elif  376.06 <= mouse[0] <= 396.06 and 410 <= mouse[1] <= 430 :
                            message = (386.06 , 420)
                        elif  689.94 <= mouse[0] <= 709.94 and 500 <= mouse[1] <= 520 :
                            message = (699.94 , 510)
                        elif  612 <= mouse[0] <= 632 and 545 <= mouse[1] <= 565 :
                            message = (622 , 555)
                        elif  847.94 <= mouse[0] <= 867.94 and 500 <= mouse[1] <= 520 :
                            message = (857.94 , 510)
                        elif  770 <= mouse[0] <= 790 and 545 <= mouse[1] <= 565 :
                            message = (780 , 555)
                        elif  1005.94 <= mouse[0] <= 1025.94 and 410 <= mouse[1] <= 430 :
                            message = (1015.94 , 420)
                        elif  1005.94 <= mouse[0] <= 1025.94 and 500 <= mouse[1] <= 520 :
                            message = (1015.94 , 510)
                        elif  928 <= mouse[0] <= 948 and 545 <= mouse[1] <= 565 :
                            message = (938 , 555)
                        elif  452.94 <= mouse[0] <= 472.94 and 635 <= mouse[1] <= 655 :
                            message = (462.94 , 645)
                        elif  375 <= mouse[0] <= 395 and 680 <= mouse[1] <= 700 :
                            message = (385 , 690) 
                        elif  297.06 <= mouse[0] <= 317.06 and 635 <= mouse[1] <= 655 :
                            message = (307.06 , 645) 
                        elif  297.06 <= mouse[0] <= 317.06 and 545 <= mouse[1] <= 565 :
                            message = (307.06 , 555) 
                        elif  610.94 <= mouse[0] <= 630.94 and 635 <= mouse[1] <= 655 :
                            message = (620.94 , 645) 
                        elif  533 <= mouse[0] <= 553 and 680 <= mouse[1] <= 700 :
                            message = (543 , 690) 
                        elif  768.94 <= mouse[0] <= 788.94 and 635 <= mouse[1] <= 655 :
                            message = (778.94 , 645) 
                        elif  691 <= mouse[0] <= 711 and 680 <= mouse[1] <= 700 :
                            message = (701 , 690) 
                        elif  926.94 <= mouse[0] <= 946.94 and 635 <= mouse[1] <= 655 :
                            message = (936.94 , 645) 
                        elif  849 <= mouse[0] <= 869 and 680 <= mouse[1] <= 700 :
                            message = (859 , 690) 
                        elif  1084.94 <= mouse[0] <= 1104.94 and 545 <= mouse[1] <= 565 :
                            message = (1094.94 , 555) 
                        elif  1084.94 <= mouse[0] <= 1104.94 and 635 <= mouse[1] <= 655 :
                            message = (1094.94 , 645 )
                        elif  1007 <= mouse[0] <= 1027 and 680 <= mouse[1] <= 700 :
                            message = (1017 , 690) 
                        elif  531.94 <= mouse[0] <= 551.94 and 770 <= mouse[1] <= 790 :
                            message = (541.94 , 780) 
                        elif  454 <= mouse[0] <= 474 and 815 <= mouse[1] <= 835 :
                            message = (464 , 825) 
                        elif  376.06 <= mouse[0] <= 396.06 and 770 <= mouse[1] <= 790 :
                            message = (386.06 , 780) 
                        elif  689.94 <= mouse[0] <= 709.94 and 770 <= mouse[1] <= 790 :
                            message = (699.94 , 780) 
                        elif  612 <= mouse[0] <= 632 and 815 <= mouse[1] <= 835 :
                            message = (622 , 825 )
                        elif  847.94 <= mouse[0] <= 867.94 and 770 <= mouse[1] <= 790 :
                            message = (857.94 , 780) 
                        elif  770 <= mouse[0] <= 790 and 815 <= mouse[1] <= 835 :
                            message = (780 , 825) 
                        elif  1005.94 <= mouse[0] <= 1025.94 and 770 <= mouse[1] <= 790 :
                            message = (1015.94 , 780) 
                        elif  928 <= mouse[0] <= 948 and 815 <= mouse[1] <= 835 :
                            message = (938 , 825) 
                        elif  609.94 <= mouse[0] <= 629.94 and 905 <= mouse[1] <= 925 :
                            message = (619.94 , 915)
                        elif  532 <= mouse[0] <= 552 and 950 <= mouse[1] <= 970 :
                            message = (542 , 960)
                        elif  454.06 <= mouse[0] <= 474.06 and 905 <= mouse[1] <= 925 :
                            message = (464.06 , 915)
                        elif  767.94 <= mouse[0] <= 787.94 and 905 <= mouse[1] <= 925 :
                            message = (777.94 , 915)
                        elif  690 <= mouse[0] <= 710 and 950 <= mouse[1] <= 970 :
                            message = (700 , 960)
                        elif  925.94 <= mouse[0] <= 945.94 and 905 <= mouse[1] <= 925 :
                            message = (935.94 , 915)
                        elif  848 <= mouse[0] <= 868 and 950 <= mouse[1] <= 970 :
                            message = (858 , 960)
        return message 

    
# ---------- INIT ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catan Board")

board = generate_catan_layout(WIDTH // 2, HEIGHT // 2)
running = True
while running:
    screen.fill((204, 173, 96))