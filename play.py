import GameFile
import gui
import gameState
game =  GameFile.Game()

gui.start_menu()
running = True

# main game loop
def main_loop(game):
    while game.running:
         command = game.carry_out_command()

    
    gui.pygame.quit()
    gui.sys.exit()