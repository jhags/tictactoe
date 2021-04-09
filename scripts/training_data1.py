''' Generate training data '''
import os
import sys

import numpy as np
import pandas as pd

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe.game import Game

nr_games = 100

history = []
win_log = []

for _ in range(nr_games):

    player, nextPlayer = -1, 1 # --> X, O

    game = Game('new')
    # game.print_board()

    while game.status == 0:

        game.play(player)
        # game.print_board()

        player, nextPlayer = nextPlayer, player

    for moveCount, boardSnapshot in game.gameHistory:
        history.append([game.winner, moveCount, boardSnapshot])

    win_log.append(game.winner)

train_data = pd.DataFrame(history, columns=['winner', 'moveCount', 'board'])

win_log = pd.DataFrame(win_log, columns=['winner'])
wl = win_log.value_counts().to_frame('games')
wl['pc_win'] = win_log.value_counts(normalize=True)

print(wl)

# Export
train_data.to_pickle(root + r'/data/game_data_{0}.pkl'.format(nr_games))
wl.to_csv(root + r'/data/game_data_winlog_{0}.csv'.format(nr_games))
