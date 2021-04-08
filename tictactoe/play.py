''' Play trained model '''
import os
import sys
import time
import numpy as np
import pandas as pd

from keras.models import load_model

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe import Game, RandomPlayer, HumanPlayer, BotPlayer

# model = load_model(root + r'/model/model_bot_randP1.h5')
model_P1 = load_model(root + r'/model/model_bot_randP1.h5')
model_P2 = load_model(root + r'/model/model_bot_randP2.h5')

lineup = [
    # (RandomPlayer(), RandomPlayer()),
    # (BotPlayer(model), RandomPlayer()),
    (RandomPlayer(), BotPlayer(model_P1)),
    # (HumanPlayer(), BotPlayer(model)),
    # (HumanPlayer(), BotPlayer(model_P2)),
    (BotPlayer(model_P1), RandomPlayer())
    # (BotPlayer(model), HumanPlayer())
    # (BotPlayer(model), BotPlayer(model, random_move_threshold=0.33)),
    # (BotPlayer(model, random_move_threshold=0.33), BotPlayer(model))
]

games = 100

winlog = []

for match in lineup:
    P1 = match[0]
    P2 = match[1]

    print(P1.name() + ' vs ' + P2.name())

    for _ in range(games):
        game = Game(P1, P2)
        game.play(print_board=False, record_history=False)

        if game.winner==0:
            winlog.append([P1.name(), P2.name(), game.winner])
        else:
            winlog.append([P1.name(), P2.name(), game.winner.nr])

winlog = pd.DataFrame(winlog, columns=['P1', 'P2', 'winner'])

results = winlog.groupby(by=['P1', 'P2', 'winner'])['winner'].count().to_frame('pc')/games
results = results.pivot_table(index=['P1', 'P2'], columns='winner', values='pc').reset_index()
results = results.rename(columns={0: 'Draw', 1: 'Win', 2: 'Lost'})

print(results)