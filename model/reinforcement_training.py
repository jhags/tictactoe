''' Play trained model '''
import os
import sys

import pandas as pd
import numpy as np

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe import BotPlayer, Game, HumanPlayer, RandomPlayer

model = np.zeros(9)
# Qtable = {}
reward = 1
learningRate = 0.1
discount = 0.9
lineup = [
    # (RandomPlayer(), RandomPlayer()),
    (BotPlayer(greedy_epsilon=0.25), RandomPlayer()),
    # (RandomPlayer(), BotPlayer(model)),
    # (HumanPlayer(), BotPlayer(model)),
    # (BotPlayer(model), HumanPlayer()),
    # (BotPlayer(model), BotPlayer(model, random_move_threshold=0.25)),
    # (BotPlayer(model, random_move_threshold=0.25), BotPlayer(model)),
]

games = 100000
log = []
for match in lineup:
    P1 = match[0]
    P2 = match[1]

    print(P1.name() + ' vs ' + P2.name())

    for game_nr in range(games):
        game = Game(P1, P2)
        game.play(print_board=False, record_history=True)

        if game.winner.value == game.player1.value:
            P1.update_model(game, reward, learningRate, discount)

        # log.append([P1.name(), P2.name(), game.winner.nr])

        if (game_nr+1)%1000==0:
            print(game_nr+1)

P1.save_model(root + r'/data/RLmodel.json')
