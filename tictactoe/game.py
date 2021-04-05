import numpy as np


class Game:

    def __init__(self, board):

        if board == 'new':
            self.board = self.new_board()
        else:
            self.board = board # np array

        self.flattened = self.board.flatten()
        # self.player = player # x/o
        self.status = None
        self.winner = None
        self.evaulate_board()

    def __str__(self):
        return str(self.print_board())

    def new_board(self):
        return np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

    def evaulate_board(self):

        rows = list(self.board.sum(axis=1))
        cols = list(self.board.sum(axis=0))
        diags_1 = self.board.trace()
        diags_2 = np.fliplr(self.board).trace()

        sums = rows + cols + [diags_1] + [diags_2]

        if 3 in sums:
            # print('Player X wins')
            self.winner = 1
            self.status = 1

        elif -3 in sums:
            # print('Player O wins')
            self.winner = -1
            self.status = 1

        else:
            # print('Game incomplete')
            self.winner = 0
            self.status = 0


    def available_moves(self):
        return np.where(self.flattened == 0)[0]


    def choose_move(self):
        available_moves = self.available_moves()
        return np.random.choice(available_moves)


    def make_move(self, player, move):
        self.flattened[move] = player
        self.board = self.flattened.reshape([3, 3])


    def player_routine(self, player, move='random'):
        if move=='random':
            move = self.choose_move()

        self.evaulate_board()
        if (self.status is None) or (self.status == 0):
            self.make_move(player, move)
            self.evaulate_board()


    def print_board(self):
        b = '''
         {0} | {1} | {2}
        ---+---+---
         {3} | {4} | {5}
        ---+---+---
         {6} | {7} | {8}
        '''

        print(b.format(*[str(x) for x in list(self.flattened)]))
