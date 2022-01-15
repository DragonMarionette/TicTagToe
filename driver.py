from Game import Game

g = Game.from_setup()
print('\n')

replay = True
while replay:
    g.play()
    replay = input('\nPlay again? (y/n): ').lower().startswith('y')
