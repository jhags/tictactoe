import os
import sys

import numpy as np
import pytest

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe.game import Game


def test_new_board():
    expected_board = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
    game = Game('new')
    np.testing.assert_array_equal(expected_board, game.board)


def test_evaluate_board():
    board = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0]
    ])

    game = Game(board)
    game.evaulate_board()
    assert game.status == 1
    assert game.winner == 1

    board = np.array([
        [1, 1, 1],
        [0, 0, 0],
        [0, 0, 0]
    ])

    game = Game(board)
    game.evaulate_board()
    assert game.status == 1
    assert game.winner == 1

    board = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    game = Game(board)
    game.evaulate_board()
    assert game.status == 1
    assert game.winner == 1

    board = np.array([
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0]
    ])

    game = Game(board)
    game.evaulate_board()
    assert game.status == 1
    assert game.winner == 1

    board = np.array([
        [1, 0, 1],
        [0, 0, 0],
        [0, 0, 0]
    ])

    game = Game(board)
    game.evaulate_board()
    assert game.status == 0
    assert game.winner == 0

    board = np.array([
        [-1, 0, 0],
        [-1, 0, 0],
        [-1, 0, 0]
    ])

    game = Game(board)
    game.evaulate_board()
    assert game.status == 1
    assert game.winner == -1

    board = np.array([
        [1, -1, 1],
        [1, 1, -1],
        [-1, 1, -1]
    ])

    game = Game(board)
    game.evaulate_board()
    assert game.status == 1
    assert game.winner == 0


    def test_make_move():
        board = np.array([
            [0, 0, 1],
            [0, 0, 0],
            [1, 0, 0]
        ])

        expected_board = np.array([
            [1, 0, 1],
            [0, 0, 0],
            [1, 0, 0]
        ])
        game = Game(board)
        game.make_move(move=0)
        np.testing.assert_array_equal(expected_board, game.board)
