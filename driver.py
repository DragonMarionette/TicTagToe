from Game import Game

player1, player2, board_size = Game.setup()
g = Game(player1, player2, board_size, turn_pause=0)
print('\n')

replay = True
while replay:
    g.play()
    replay = input('\nPlay again? (y/n): ').lower().startswith('y')
