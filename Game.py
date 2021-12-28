from time import sleep
from random import randint

import AI
import Recur
from Board import GameBoard, X, O
from Player import Player, Human
import dialog


class Game:
    def __init__(self, p1: Player, p2: Player, board_size: int, turn_pause: int = 2):
        self.players = p1, p2
        self.board = GameBoard(board_size)
        self.turn_pause = turn_pause

    # Play through a game with p1 and p2 on board
    def play(self, verbose=True):
        self.board.clear()
        if verbose:
            self.board.print()
        turn = 1
        while not self.board.check(self.players[turn].char):  # while last player to move has not won
            if self.board.full():
                if verbose:
                    print('It\'s a tie!')
                return None

            turn = (turn + 1) % 2
            if verbose:
                sleep(self.turn_pause)
                print(f'It is now {self.players[turn].name}\'s turn.')

            self.players[turn].move(self.board)

            if verbose:
                self.board.print()

        if verbose:
            print(f'{self.players[turn].name} wins!')
        return self.players[turn]

    # Take user input and return (Player, Player, n)
    @staticmethod
    def setup():
        n = dialog.validate_int('\nHow tall should the board be? Enter a number: ', lowest=1, highest=10)

        gametype_options = {
            1: 'Human vs. Human',
            2: 'Human vs. Computer',
            3: 'Computer vs. Computer'
        }
        gametype, _ = dialog.from_intdict(gametype_options, prompt='\nWho will be playing?')

        if gametype == 1:
            p1 = Game.establish_human(X, 'first')
            p2 = Game.establish_human(O, 'second')
        elif gametype == 2:
            p1 = Game.establish_human(X, 'human')
            p2 = Game.establish_ai(O, 'AI')
        else:  # game_type == 3
            p1 = Game.establish_ai(X, 'first')
            p2 = Game.establish_ai(O, 'second')

        order_options = {
            1: p1.name,
            2: p2.name,
            3: 'Choose randomly'
        }

        who_first, _ = dialog.from_intdict(order_options, prompt='\nWhich player should go first?')

        if who_first == 3:
            who_first = randint(1, 2)
        if who_first == 2:
            p1, p2 = p2, p1

        return p1, p2, n

    @staticmethod
    def from_setup():
        p1, p2, n = Game.setup()
        return Game(p1, p2, n)

    @staticmethod
    def establish_human(c: int, adjective: str):
        name = input(f'\nPlease input a name for the {adjective} player: ')
        return Human(name, c)

    @staticmethod
    def establish_ai(c: int, adjective: str):
        ai_options = {
            1: AI.Random(c),
            2: AI.OneAhead(c),
            3: Recur.Recursive(c)
        }
        _, ai_choice = dialog.from_intdict(ai_options, f'\nChoose the {adjective} player')
        return ai_choice
