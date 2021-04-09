''' Play trained model '''
import os
import sys

import pandas as pd
import numpy as np

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe import BotPlayer, Game, HumanPlayer, RandomPlayer, simulate

rewards = [3, 1, -10]
learningRate = 0.1
discount = 0.8
games = 25000

lineup = [
    (BotPlayer(player1=True, greedy_epsilon=0.4), RandomPlayer()),
    # (RandomPlayer(), BotPlayer(player1=False, greedy_epsilon=0.2)),
]

log = []
for match in lineup:
    P1 = match[0]
    P2 = match[1]

    print(P1.name() + ' vs ' + P2.name())

    for game_nr in range(games):
        game = Game(P1, P2)
        game.play(print_board=False, record_history=True)

        P1.update_model(game, rewards, learningRate, discount)

        if (game_nr+1)%100==0:
            simulate([BotPlayer(model=P1.model), RandomPlayer()], 100)

P1.save_model(root + r'/model/RLmodel_P1.json')
