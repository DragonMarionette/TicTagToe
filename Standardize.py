from copy import deepcopy
from itertools import permutations
import numpy as np

from Board import GameBoard


# Gives the standardized scramble of a GameBoard b
# Returns (scrambled GameBoard, description of the scramble permutation, hash of the scrambled GameBoard)
def scramble(b: GameBoard, naive: bool = True):
    if naive:
        return scramble_naive(b)
    else:
        return scramble_efficient(b)


# Gives the standardized scramble of a GameBoard b
# Returns (scrambled GameBoard, description of the scramble permutation, hash of the scrambled GameBoard)
# Horribly inefficient as there are 2(n!)^2 arrangements
def scramble_naive(b: GameBoard):
    to_concat = (np.indices(b.grid.shape), np.expand_dims(deepcopy(b.grid), axis=0))
    representation = np.concatenate(to_concat)  # n-by-n-by-3 grid representing indices and content of the spaces

    all_equivalents = []
    row_perms = permutations(range(b.n))
    for r in row_perms:
        row_permuted = representation[:, r, :]

        col_perms = permutations(range(b.n))
        for c in col_perms:
            all_equivalents.append(row_permuted[:, :, c])
    transposed = [np.transpose(g, axes=(0, 2, 1)) for g in all_equivalents]
    all_equivalents += transposed

    out_vals = min(all_equivalents, key=lambda x: x[2].tolist())
    board_out = GameBoard(0, grid=out_vals[2])

    return board_out, out_vals[0:2, :, :], hash(board_out)


# Gives the standardized scramble of a GameBoard b
# Returns (scrambled GameBoard, description of the scramble permutation, hash of the scrambled GameBoard)
# Will be somewhat more efficient, but I think this is an NP problem.
def scramble_efficient(b: GameBoard):  # TODO: write this (replacing naive code)
    return scramble_naive(b)


# Takes an n-by-n-by-2 array and a scramble permutation of an n-by-n GameBoard
# Returns the unscrambled version of the array, treating input as though it were the result of the given scramble
def unscramble(grid: np.ndarray, permutation: np.ndarray, debug=False) -> np.ndarray:
    out_arr = np.empty_like(grid)
    for i in range(out_arr.shape[0]):
        for j in range(out_arr.shape[0]):
            out_arr[permutation[1, i, j], permutation[0, i, j]] = grid[j, i]

    if debug:
        print(f'2 scrambled=\n{grid}')
        print(f'2 unscrambled=\n{out_arr}')

    return out_arr
