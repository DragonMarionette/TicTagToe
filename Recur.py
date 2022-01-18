import numpy as np
from random import choice

from AI import AI
from Board import GameBoard
import Standardize
import Token

# Done: instead of constructing hypo_board, modify sub_board in place. Negligible speedup but ~halves memory use
# Done: aggressive pruning such that the first winning strategy found is used
# TODO: allow termination at lower depth using imperfect evaluation function
# TODO: remember previous calculations
# TODO: choose *better* moves that give opponent more chance to slip up


class Recursive(AI):
    character_name = 'The Lazy Oracle'

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

            if sub_board.empty() == 1:  # if last move of game
                space = sub_board.legal_spaces()[0]  # always (0, 0) with current Standardize.scramble()
                sub_board.place(c, space)
                space_ratings[space] = int(sub_board.check(c))  # 1 if c wins, 0 if it's a tie
                sub_board.replace(Token.EMPTY, space)

            else:  # not last move of game
                break_early = False
                for space in sub_board.legal_spaces():  # for each legal space:
                    sub_board.place(c, space)
                    if sub_board.check(c):  # if c wins at space, space's rating is 1
                        space_ratings[space] = 1
                        break_early = True  # no need to check recursively if possible to win this turn
                        sub_board.replace(Token.EMPTY, space)
                        break
                    sub_board.replace(Token.EMPTY, space)

                if not break_early:  # if no immediate wins found, minimax
                    for space in sub_board.legal_spaces():  # for each legal space:
                        sub_board.place(c, space)
                        next_down = self.helper(not c, sub_board)
                        space_ratings[space] = -np.amax(next_down)
                        sub_board.replace(Token.EMPTY, space)
                        if space_ratings[space] == 1:
                            break

            self._board_states[state_id] = space_ratings

        return Standardize.unscramble(space_ratings, permutation)
