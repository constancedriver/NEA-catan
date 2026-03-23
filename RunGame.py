import GameFile
import GuiFile
import BotFile

# main game loop
def main_loop(game):
    while game.running:
        game.game_end()#
        if game.state.currentScreen == 'main menu':
            command = GuiFile.command(game.state.currentScreen)
        elif not (game.state.currentScreen != 'main menu' and game.players[game.turnIndex].isBot):
            command = GuiFile.command(game.state.currentScreen)
        else:
            command = BotFile.turn(game)
        if command != None: # only compares commad type if a command is returned
            if command['TYPE'] == 'visual':
                if command['COMMAND'] == 'exit rules' and game.state.currentScreen == 'game':
                    action = game.load_game_screen()
                elif command['COMMAND'] == 'exit rules' and game.state.currentScreen == 'place starting pieces':
                    action = game.load_starting_screen()
                else:
                    #handel in game state
                    action = game.state.get_command(command)
            elif command['TYPE'] == 'prog':
                #handel in game file
                action = game.carry_out_command(command)
            if action is None:
                print('ERROR: couldnt find command')
            else: 
                action()
            if len(game.state.pressedNodes) == 2:
                game.build()
    BotFile.make_board(game)
    print(BotFile.board)    
    
    GuiFile.pygame.quit()
    GuiFile.sys.exit()

#calling game 
game =  GameFile.Game()    
GuiFile.start_menu()
main_loop(game)
print(BotFile.board)