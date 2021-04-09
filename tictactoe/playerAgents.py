''' Types of Players Class '''

# from keras.utils import np_utils
import json
import random

import numpy as np


class Player:

    def __init__(self, agent, player_nr, token, value):
        self.agent = agent
        self.nr = player_nr
        self.token = token
        self.value = value

    def __repr__(self):
        return self.__class__.__name__ + str(self.nr)


class RandomPlayer:

    def name(self):
        return self.__class__.__name__

    def choose_move(self, available_moves):
        return np.random.choice(available_moves)


class HumanPlayer:

    def name(self):
        return self.__class__.__name__

    def choose_move(self, available_moves):
        move = input('Your turn. Available moves: %s.' % str(available_moves))
        if move=='':
            return self.choose_move(available_moves)
        return int(move)


class BotPlayer:

    def __init__(self, player1=True, model=None, greedy_epsilon=None):

        self.player1 = True
        if player1 is True:
            self.player_nr = 1
        else:
            self.player_nr = 2

        if model is None:
            self.model = {}
        else:
            self.model = model

        self.rand_threshold = greedy_epsilon
        self.random_move = False

    def name(self):
        return self.__class__.__name__

    def make_random_move(self):
        val = random.random()
        if val < self.rand_threshold:
            self.random_move = True
        else:
            self.random_move = False

    def choose_move(self, available_moves, board=None):
        if self.rand_threshold is not None:
            self.make_random_move()

        if self.random_move is False:
            # predict_moves = self.model.predict(np.array([board]))
            # moves = predict_moves[0][available_moves]
            # idx = np.argmax(moves)
            # move = available_moves[idx]

            hashBoard = ''.join(list(board.astype(str)))
            if hashBoard in self.model:
                actions = self.model[hashBoard]
            else:
                return np.random.choice(available_moves)

            ordered_moves = list(reversed(np.argsort(actions)))
            for move in ordered_moves:
                if move in available_moves:
                    break
            return int(move)

        elif self.random_move is True:
            return np.random.choice(available_moves)


    def update_model(self, game, rewards, learningRate, discount):
        # Set reward based on game outcome
        if game.winner.nr==self.player_nr: # WON
            Qval = rewards[0]
        elif game.winner.nr==0: # DRAW
            Qval = rewards[1]
        else:
            Qval = rewards[2]

        # Qval = reward
        for move in reversed(game.gameHistory):
            # only interested in this player's move
            if move[2].nr==self.player_nr:
                cell = move[3]
                hashBoard = ''.join(list(move[1].astype(str)))
                if hashBoard in self.model:
                    actions = self.model[hashBoard]
                else:
                    actions = np.zeros(9)

                Qval = ((Qval * discount))
                actions[cell] = actions[cell] + (Qval * learningRate)

                self.model[hashBoard] = actions

    def save_model(self, filepath):
        for k, v in self.model.items():
            self.model[k] = list(v)
        json.dump(self.model, open(filepath, 'w'))