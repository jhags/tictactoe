import numpy as np


class Game:

    def __init__(self, board):

        if isinstance(board, str):
            if board == 'new':
                self.board = self.new_board()

        elif isinstance(board, np.ndarray):
            self.board = board # np array

        self.flattened = self.board.flatten()
        self.status = None
        self.winner = None
        self.gameHistory = []
        self.moveCounter = 0
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

        if -3 in sums:
            # print('Player X wins')
            self.winner = 'X'
            self.status = 1

        elif 3 in sums:
            # print('Player O wins')
            self.winner = 'O'
            self.status = 1

        elif len(np.where(self.flattened == 0)[0]) == 0:
            self.winner = 'D'
            self.status = 1

        else:
            # print('Game incomplete')
            self.winner = None
            self.status = 0


    def available_moves(self):
        return np.where(self.flattened == 0)[0]


    def choose_move(self, player=None, method='random', model=None):
        available_moves = self.available_moves()

        if method=='random':
            return np.random.choice(available_moves)

        elif method=='bot':
            playerMap = {-1: 0, 1: 1}

            best_off = []
            best_def = []
            for p in [-1, 1]:
                possible_moves = []
                for move in available_moves:
                    nextMove = Game(self.board)
                    nextMove.make_move(p, move)
                    possible_moves.append(nextMove.flattened)

                predict_move = model.predict(np.vstack(possible_moves))[:, playerMap[p]]
                # print(np.round(predict_move, 2))

                prob = np.max(predict_move)
                idx = np.argmax(predict_move)
                if p==player:
                    best_off.append(prob)
                    best_off.append(idx)
                elif p!=player:
                    best_def.append(prob)
                    best_def.append(idx)

            if best_off[0] >= best_def[0]:
                idx = best_off[1]
            else:
                idx = best_def[1]
            return available_moves[idx]

    def make_move(self, player, move):
        self.flattened[move] = player
        self.board = self.flattened.reshape([3, 3])


    def play(self, player, method='random', model=None):

        self.evaulate_board()

        if (self.status is None) or (self.status == 0):

            if method=='random':
                move = self.choose_move()

            elif method=='bot':
                move = self.choose_move(player=player, method=method, model=model)

            elif method=='human':
                move = input('You are player %s. Enter cell number (0 to 8).' % str(player))
                move = int(move)

            self.make_move(player, move)
            self.moveCounter += 1
            self.gameHistory.append([self.moveCounter, self.flattened.copy()])
            self.evaulate_board()


    def print_board(self):
        b = '''
         {0} | {1} | {2}
        ---+---+---
         {3} | {4} | {5}
        ---+---+---
         {6} | {7} | {8}
        '''

        markerMap = {-1: 'X', 1: 'O', 0: ' '}

        strBoard = [markerMap[x] for x in self.flattened]

        print(b.format(*strBoard))
