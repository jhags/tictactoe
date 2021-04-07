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

model = load_model(root + r'/model/model_5.h5')

win_log = []

best_of = 3

for match in range(best_of):
    print(match)

    player, nextPlayer = 1, -1 # --> X, O

    game = Game('new')
    game.print_board()

    while game.status == 0:
        if player==1:
            game.play(player,  method='human')
            game.print_board()

        elif player==-1:
            game.play(player,  method='bot', model=model)
            game.print_board()

        player, nextPlayer = nextPlayer, player

    win_log.append(game.winner)


win_log = pd.DataFrame(win_log, columns=['winner'])
wl = win_log.value_counts().to_frame('games')
wl['pc_win'] = win_log.value_counts(normalize=True)
