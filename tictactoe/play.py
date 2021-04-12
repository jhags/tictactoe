''' Play trained model '''
import json
import os
import sys
import time

import numpy as np
import pandas as pd
from keras.models import load_model

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe import BotPlayer, Game, HumanPlayer, RandomPlayer

P1model = json.load(open(root + r'/model/RLmodel_P1.json'))
for k, v in P1model.items():
    P1model[k] = np.array(v)

P2model = json.load(open(root + r'/model/RLmodel_P2.json'))
for k, v in P2model.items():
    P2model[k] = np.array(v)

lineup = [
#     (HumanPlayer(), BotPlayer(model=P2model)),
    (BotPlayer(model=P1model), HumanPlayer())
]

games = 3

winlog = []

for match in lineup:
    P1 = match[0]
    P2 = match[1]

    print(P1.name() + ' vs ' + P2.name())

    for _ in range(games):
        game = Game(P1, P2)
        game.play(print_board=True, record_history=False)

        winlog.append([P1.name(), P2.name(), game.winner.nr])

winlog = pd.DataFrame(winlog, columns=['P1', 'P2', 'winner'])

results = winlog.groupby(by=['P1', 'P2', 'winner'])['winner'].count().to_frame('pc')/games
results = results.pivot_table(index=['P1', 'P2'], columns='winner', values='pc').reset_index()
results = results.rename(columns={0: 'Draw', 1: 'Win', 2: 'Lost'})

print(results)
