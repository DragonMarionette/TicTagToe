from copy import deepcopy
import numpy as np
from random import choice

from AI import AI, legal_spaces
from Board import GameBoard
import Standardize
import Token

# Done: optimizing redundant branches. Used dict
# Done: optimizing equivalent branches. Used dict
# Done: instead of constructing hypo_board, modified sub_board in place. Did not improve performance; reverted
# TODO: allow termination at lower depth using imperfect evaluation function
# TODO: remember previous calculations
# TODO: alpha-beta pruning
# TODO: choose *better* moves that give opponent more chance to slip up


class Recursive(AI):
    character_name = 'The Oracle'

    def __init__(self, char):
        super().__init__(Recursive.character_name, char)
        self._board_states = dict()

    def choose_space(self, b: GameBoard, verbose: bool = False):
        space_ratings = self.helper(self.char, b)
        if verbose:
            print(f"space_ratings =\n{space_ratings.transpose()}")  # for debugging purposes
        best_option = np.amax(space_ratings)
        cols, rows = np.where(space_ratings == best_option)  # This is the correct row/col order, I checked
        viable_spaces = list(zip(cols, rows))

        move = choice(viable_spaces)
        if verbose:
            print(f"{self.name} went in "
                  f"{chr(move[0] + ord('A'))}"
                  f"{move[1]+1}")  # for debugging purposes
        return move

    def helper(self, c: int, in_board: GameBoard):
        sub_board, permutation, state_id = Standardize.scramble(in_board, naive=False)
        state_id = hash(sub_board)

        if state_id in self._board_states:
            space_ratings = self._board_states[state_id]
        else:
            space_ratings = np.full(sub_board.grid.shape, -2, dtype=np.short)  # spaces default to illegal

            hypo_board = deepcopy(sub_board)
            for space in legal_spaces(sub_board):  # for each legal space:
                hypo_board.place(c, space)
                if hypo_board.check(c):  # if c wins at space, space's rating is 1
                    space_ratings[space] = 1
                elif hypo_board.full():  # if it's a tie, space's rating is 0
                    space_ratings[space] = 0
                else:
                    next_down = self.helper(not c, hypo_board)
                    space_ratings[space] = -np.amax(next_down)
                hypo_board.replace(Token.EMPTY, space)

            self._board_states[state_id] = space_ratings

        return Standardize.unscramble(space_ratings, permutation)
