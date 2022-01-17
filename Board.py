import numpy as np
import re

import Token


valid_players = (Token.X, Token.O)


class Board:
    def __init__(self, size: int, grid: np.ndarray = None):
        if grid is not None:
            self._grid = grid
            self._n = grid.shape[0]
        else:
            assert size <= 9
            self._n = size
            self._grid = np.full((size, size), Token.EMPTY, dtype=np.int8)

    # Dimension of the grid
    @property
    def n(self) -> int:
        return self._n

    # Numpy array of player pieces, stored as ints
    @property
    def grid(self) -> np.ndarray:
        return self._grid

    def __getitem__(self, item):
        return self.grid[item]

    def __hash__(self):
        return hash(tuple(self._grid.flatten()))

    # Attempt to place `player` piece at `coord`. Return False if space was occupied and abort
    def place(self, player: int, coord) -> bool:
        x, y = coord
        if not 0 <= x < self.n:
            raise IndexError('Illegal column index')
        elif not 0 <= y < self.n:
            raise IndexError('Illegal row index')
        if not isinstance(player, int):
            raise TypeError(f'Expected int, instead found {type(player)}')

        if self._grid[y, x] == Token.EMPTY:
            self._grid[y, x] = player
            return True
        else:
            return False

    # Place `player` piece at `coord` even if it replaces another piece
    def replace(self, player: int, coord) -> bool:
        x, y = coord
        if not 0 <= x < self.n:
            raise IndexError('Illegal column index')
        elif not 0 <= y < self.n:
            raise IndexError('Illegal row index')
        if not isinstance(player, int):
            raise TypeError(f'Expected int, instead found {type(player)}')

        self._grid[y, x] = player
        return True

    # Reset the board to empty
    def clear(self):
        self._grid.fill(Token.EMPTY)

    # Return true if `player` has won, else False
    def check(self, player: int) -> bool:
        def check_helper(g: np.ndarray):
            if g.size == 0:
                return True
            for i in range(g.shape[0]):  # for each row number
                if g[0, i] == player:  # if we've found the correct letter in the 0th column of this row
                    smaller = np.delete(g[1:, :], i, axis=1)  # construct smaller array without that row or column
                    if check_helper(smaller):
                        return True
            return False

        assert player in valid_players
        return check_helper(self.grid)

    # Replace all X with O and vice versa
    # def invert(self):  # TODO: test
    #     transformation = {
    #         Token.X: Token.O,
    #         Token.O: Token.X,
    #         Token.EMPTY: Token.EMPTY
    #     }
    #     with np.nditer(self._grid, op_flags=['readwrite']) as it:
    #         for space in it:
    #             space[...] = transformation[Token.X]


class GameBoard(Board):

    # Return printable character at coordinate, as would be visible during board printing
    def char_at(self, coordinate) -> str:
        x, y = coordinate
        c = self.grid[y, x]
        return Token.colors[c] + Token.symbols[c] + '\033[0m'

    # From input of the form 'A1' or '1A', return (x, y) indices on grid. Not case sensitive
    def coord(self, space: str):
        space = space.lower()
        if re.fullmatch(r'\d[a-z]', space):
            row = space[0]
            col = space[1]
        elif re.fullmatch(r'[a-z]\d', space):
            col = space[0]
            row = space[1]
        else:
            raise ValueError

        row = int(row) - 1
        col = ord(col) - ord('a')

        if not 0 <= col < self.n:
            raise IndexError('Column')
        elif not 0 <= row < self.n:
            raise IndexError('Row')
        return col, row

    # Return True if `coordinate` on grid has a player piece in it, else False
    def occupied(self, coordinate):
        x, y = coordinate
        return self.grid[y, x] != Token.EMPTY

    # Return True if board has no empty spaces
    def full(self):
        return not np.any(self.grid == Token.EMPTY)

    # Return number of empty spaces
    def empty(self):
        return len(self.grid[self.grid == Token.EMPTY])

    # Return number of nonempty spaces
    def nonempty(self):
        return len(self.grid[self.grid != Token.EMPTY])

    # Print board to console
    def print(self):
        print('  ', end='')

        for col in range(self.n):  # column headers
            print(f'\u005F{chr(col + ord("A"))}\u005F', end='')
        print()

        for row in range(self.n):  # for each row
            print(f'{row + 1}\u00A6', end='')  # row headers
            for col in range(self.n):
                print(f' {self.char_at((col, row))} ', end='')
            print('\u00A6')  # final pipe

        print('  ', end='')  # bottom line
        for col in range(self.n):
            print('\u00AF'*3, end='')
        print()
