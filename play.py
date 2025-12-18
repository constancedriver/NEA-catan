from game import *
game1 =  Game()
game1.start_game()
while not game1.won():
    game1.roll_dice()
    # do turn things
    game1.next_turn()
#game1.game_end()