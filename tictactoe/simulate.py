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


def simulate(lineup, games):
    winlog = []

    P1 = lineup[0]
    P2 = lineup[1]

    for _ in range(games):
        game = Game(P1, P2)
        game.play(print_board=False, record_history=False)

        winlog.append([P1.name(), P2.name(), game.winner.nr])

    winlog = pd.DataFrame(winlog, columns=['P1', 'P2', 'winner'])

    wins = round(100*len(winlog[winlog['winner']==1])/games, 1)
    lost = round(100*len(winlog[winlog['winner']==2])/games, 1)
    draw = round(100*len(winlog[winlog['winner']==0])/games, 1)
    print('W: {} | D: {} | L: {}'.format(wins, draw, lost))


if __name__ == "__main__":
    lineup = [RandomPlayer(), RandomPlayer()]
    games = 5
    simulate(lineup, games)
