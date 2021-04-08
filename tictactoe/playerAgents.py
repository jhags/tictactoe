''' Types of Players Class '''

import numpy as np
import random
from keras.utils import np_utils

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

    def __init__(self, model, random_move_threshold=None):
        self.model = model
        self.rand_threshold = random_move_threshold
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
            predict_moves = self.model.predict(np.array([board]))
            moves = predict_moves[0][available_moves]
            idx = np.argmax(moves)
            move = available_moves[idx]
            return int(move)

        elif self.random_move is True:
            return np.random.choice(available_moves)
