from copy import deepcopy
from random import choice

from Board import GameBoard
from Player import Player


# Template class for any AI strategy
class AI(Player):
    character_name = 'Generic AI'

    def __init__(self, name, char):
        super().__init__(name, char)

    def move(self, b: GameBoard):
        b.place(self.char, self.choose_space(b))

    def choose_space(self, b: GameBoard):
        return None, None

    @staticmethod
    def random(b: GameBoard):
        return choice(b.legal_spaces())


# Strategy: move in a random legal spot
class Random(AI):
    character_name = 'Randominic the Unpredictable'

    def __init__(self, char):
        super().__init__(Random.character_name, char)

    def choose_space(self, b: GameBoard):
        return self.random(b)


# Strategy: look one move ahead. Win if possible, else block if possible, else move randomly
class OneAhead(AI):
    character_name = 'Sir Plansalittle'

    def __init__(self, char):
        super().__init__(OneAhead.character_name, char)

    def choose_space(self, b: GameBoard):
        can_win = False
        viable_spaces = []
        for space in b.legal_spaces():
            hypothetical_board = deepcopy(b)

            hypothetical_board.place(self.char, space)
            if hypothetical_board.check(self.char):
                if not can_win:
                    viable_spaces.clear()
                    can_win = True
                viable_spaces.append(space)
            elif not can_win:
                hypothetical_board.replace(not self.char, space)
                if hypothetical_board.check(not self.char):
                    viable_spaces.append(space)
        if viable_spaces:
            return choice(viable_spaces)
        else:
            return self.random(b)


class Heuristic(AI):
    character_name = 'Hugh'

    def __init__(self, char):
        super().__init__(Heuristic.character_name, char)

    def choose_space(self, b: GameBoard):
        return self.random(b)


class TwoAhead(AI):  # TODO
    def __init__(self, char):
        super().__init__('Mrs. Doubleday', char)

    def choose_space(self, b: GameBoard):
        return self.random(b)


class Offensive(AI):  # TODO
    def __init__(self, char):
        super().__init__('Striker', char)

    def choose_space(self, b: GameBoard):
        return self.random(b)


class Defensive(AI):  # TODO
    def __init__(self, char):
        super().__init__('Dede', char)

    def choose_space(self, b: GameBoard):
        return self.random(b)


class Paper(AI):  # TODO: implement the strategy described in paper claiming to have solved the game
    def __init__(self, char):
        super().__init__('Niranjan Krishna', char)

    def choose_space(self, b: GameBoard):
        return self.random(b)
