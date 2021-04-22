import json
import pathlib
import random

import numpy as np


def select_move(board, player_turn, difficulty):
    """Select the best move to make

    Args:
        board (str): string of 9 characters representing the current board state e.g. 012012012 where 0 are blank cells, 1 is X and 2 is O
        player_turn (str): either 'X' or 'O'. X will be converted to 1, O to 2.
        difficulty (str): easy, medium or hard. This modifies the greedy epsilon random move threshold.

    Returns:
        int: selected move (0 to 8)
    """

    board_arr = np.array([int(char) for char in board])

    fpath = pathlib.Path(__file__).parent
    if player_turn=='X':
        model = load_model(fpath / 'P1model.json')
    elif player_turn=='O':
        model = load_model(fpath / 'P2model.json')
    else:
        pass

    difficulty_levels = {
        'hard': 0,
        'medium': 0.75,
        'easy': 0.5
    }
    random_threshold = difficulty_levels[difficulty.lower()]

    available_moves = get_available_moves(board_arr)

    val = random.random()
    if val < random_threshold:
        return int(np.random.choice(available_moves))

    if board in model:
        actions = model[board]
    else:
        return int(np.random.choice(available_moves))

    ordered_moves = list(reversed(np.argsort(actions)))
    for move in ordered_moves:
        if move in available_moves:
            break
    return int(move)


def load_model(model_path):

    model = json.load(open(model_path))
    for k, v in model.items():
        model[k] = np.array(v)

    return model


def get_available_moves(arrboard):
    return np.where(arrboard == 0)[0]
