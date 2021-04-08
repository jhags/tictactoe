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

    def __init__(self, model=None, greedy_epsilon=None):
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


    def update_model(self, game, reward, learningRate, discount):
        Qval = reward
        for move in reversed(game.gameHistory):
            if move[2].value==game.player1.value:
                cell = move[3]
                hashBoard = ''.join(list(move[1].astype(str)))
                if hashBoard in self.model:
                    actions = self.model[hashBoard]
                else:
                    actions = np.zeros(9)

                Qval = ((Qval * discount) - actions[cell])
                actions[cell] = Qval * learningRate

                self.model[hashBoard] = actions

    def save_model(self, filepath):
        for k, v in self.model.items():
            self.model[k] = list(v)
        json.dump(self.model, open(filepath, 'w'))