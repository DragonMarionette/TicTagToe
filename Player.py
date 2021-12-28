from Board import GameBoard
import Token


class Player:
    def __init__(self, name, char):
        self.name = Token.colors[char] + name + '\033[0m'
        self._char = char

    @property
    def char(self):
        return self._char

    def move(self, board: GameBoard):
        pass

    def __str__(self):
        return self.name


class Human(Player):
    def move(self, board: GameBoard):
        while True:
            space = input(f'{self.name}, choose a space for your move: ')
            legal = True
            reason = 'Move is legal'

            try:
                if not board.place(self.char, board.coord(space)):
                    legal = False
                    reason = f'Space {space} is already filled'
            except ValueError:
                legal = False
                reason = 'Input cannot be parsed as a space on the board'
            except IndexError as ind:
                legal = False
                reason = ind.args[0] + ' is out of bounds'

            if legal:
                break
            else:
                print(reason + '. Please try again.')

