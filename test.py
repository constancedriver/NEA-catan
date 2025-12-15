players = ['w', 'b', 'r', 'o']
playerIndex = 2
for i in range (len(players)):
    playerIndex -= 1
    if playerIndex < 0:
        playerIndex = 3
    print(players[playerIndex])
