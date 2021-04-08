import numpy as np
import pprint

from .playerAgents import Player

class Game:

    def __init__(self, player1, player2, player1_to_move=True, board=None):

        self.player1 = Player(player1, 1, 'X', 1)
        self.player2 = Player(player2, 2, 'O', 2)
        self.draw = Player(None, 0, None, 0)

        if player1_to_move:
            self.currPlayer = self.player1
            self.nextPlayer = self.player2
        else:
            self.currPlayer = self.player2
            self.nextPlayer = self.player1

        if board is None:
            self.board = self.new_board()
        else:
            self.board = board.flatten()

        self.status = None
        self.winner = None
        self.gameHistory = []
        self.moveCounter = 0
        self.evaulate_board()


    def new_board(self):
        new_board = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        return new_board.flatten()


    def evaulate_board(self):

        arrBoard = self.board.copy() # make a copy
        arrBoard = np.where(arrBoard==self.player1.value, -1, arrBoard) # Replace P1 with -1
        arrBoard = np.where(arrBoard==self.player2.value, 1, arrBoard) # Replace P2 with 1

        arrBoard = arrBoard.reshape(3, 3)
        rows = list(arrBoard.sum(axis=1))
        cols = list(arrBoard.sum(axis=0))
        diags_1 = arrBoard.trace()
        diags_2 = np.fliplr(arrBoard).trace()

        sums = rows + cols + [diags_1] + [diags_2]

        if -3 in sums: # X wins
            self.winner = self.player1
            self.status = 1

        elif 3 in sums: # O wins
            self.winner = self.player2
            self.status = 1

        elif len(np.where(self.board == 0)[0]) == 0: # Draw
            self.winner = self.draw
            self.status = 1

        else: # Game in progress
            self.winner = None
            self.status = 0


    def available_moves(self):
        return np.where(self.board == 0)[0]


    def make_move(self, move, player_value):
        self.board[move] = player_value


    def play(self, print_board=True, record_history=True):

        moveCounter = 0
        history = []

        while self.status==0:
            moveCounter+=1

            if print_board:
                self.print_playermessage()
                self.print_board()

            available_moves = self.available_moves()

            if self.currPlayer.agent.name()=='BotPlayer':
                move = self.currPlayer.agent.choose_move(available_moves, board=self.board)
            else:
                move = self.currPlayer.agent.choose_move(available_moves)

            if record_history:
                history.append([
                    moveCounter,
                    self.board.copy(),
                    self.currPlayer,
                    move
                    ])

            self.make_move(move, self.currPlayer.value)

            self.evaulate_board()

            # Swap current Player
            self.currPlayer, self.nextPlayer = self.nextPlayer, self.currPlayer

        if self.status==1:
            if print_board:
                self.print_board()
                self.print_evaluationmessage()

            if record_history:
                for item in history:
                    # History cols:
                    # move; board; player nr; player token; player value, player move; winner
                    self.gameHistory.append(item + [self.winner])


    def print_board(self):
        b = '''
         {0} | {1} | {2}    0   1   2
        ---+---+---
         {3} | {4} | {5}    3   4   5
        ---+---+---
         {6} | {7} | {8}    6   7   8
        '''

        markerMap = {
            self.player1.value: self.player1.token,
            self.player2.value: self.player2.token,
            0: ' '}

        strBoard = [markerMap[x] for x in self.board]

        print(b.format(*strBoard))


    def print_playermessage(self):

        print("Player {} / {} ({}). Your turn.".format(
            str(self.currPlayer.nr),
            self.currPlayer.agent.name(),
            self.currPlayer.token))


    def print_evaluationmessage(self):

        if self.winner.value==0:
            print('Draw!\n=== GAME OVER ===')

        else:
            print("Player {} / {} ({}) wins!\n=== GAME OVER ===".format(
                str(self.winner.nr),
                self.winner.agent.name(),
                self.winner.token))
