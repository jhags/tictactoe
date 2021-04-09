''' Play trained model '''
import os
import sys
import time
import numpy as np
import pandas as pd

from keras.models import load_model

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe.game import Game

training_iteration = 5

model = load_model(root + r'/model/model_%s.h5' % (str(training_iteration-1)))

nr_games = 100

history = []
win_log = []

matches = [
    ('bot', 'bot'),
    ('bot', 'random'),
    ('random', 'bot'),
    # ('random', 'random')
]

for match in matches:
    print(match)

    for _ in range(nr_games):

        player, nextPlayer = 1, -1 # --> X, O
        game = Game('new')

        while game.status == 0:
            if player==1:
                game.play(player,  method=match[0], model=model)

            elif player==-1:
                game.play(player,  method=match[1], model=model)

            player, nextPlayer = nextPlayer, player

        win_log.append(game.winner)

        for moveCount, boardSnapshot in game.gameHistory:
            history.append([game.winner, moveCount, boardSnapshot])

train_data = pd.DataFrame(history, columns=['winner', 'moveCount', 'board'])

win_log = pd.DataFrame(win_log, columns=['winner'])
wl = win_log.value_counts().to_frame('games')
wl['pc_win'] = win_log.value_counts(normalize=True)

train_data.to_pickle(root + r'/data/data_{0}.pkl'.format(str(training_iteration)))
