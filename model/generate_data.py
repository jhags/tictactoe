''' Play trained model '''
import os
import sys

import pandas as pd
import numpy as np
from keras.models import load_model

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe import BotPlayer, Game, HumanPlayer, RandomPlayer

model = load_model(root + r'/model/model.h5')

lineup = [
    (RandomPlayer(), RandomPlayer()),
    # (BotPlayer(model), RandomPlayer()),
    # (RandomPlayer(), BotPlayer(model)),
    # (HumanPlayer(), BotPlayer(model)),
    # (BotPlayer(model), HumanPlayer()),
    # (BotPlayer(model), BotPlayer(model, random_move_threshold=0.25)),
    # (BotPlayer(model, random_move_threshold=0.25), BotPlayer(model)),
]

games = 100000

log = []
winlog = []
for match in lineup:
    P1 = match[0]
    P2 = match[1]

    print(P1.name() + ' vs ' + P2.name())

    for game_nr in range(games):
        game = Game(P1, P2)
        game.play(print_board=False, record_history=True)

        for move in game.gameHistory:
            log.append([game_nr] + move)

        if game.winner==0:
            winlog.append([P1.name(), P2.name(), game.winner])
        else:
            winlog.append([P1.name(), P2.name(), game.winner.nr])

# Evaulate win results
winlog = pd.DataFrame(winlog, columns=['P1', 'P2', 'winner'])
results = winlog.groupby(by=['P1', 'P2', 'winner'])['winner'].count().to_frame('pc')/games
results = results.pivot_table(index=['P1', 'P2'], columns='winner', values='pc').reset_index()
results = results.rename(columns={0: 'Draw', 1: 'Win', 2: 'Lost'})

print(results)

# Training data
# Normalise perspectives

# def mirror_board(board, move, flip_axis, playerVal):
#     m = np.zeros(9).astype(int)
#     m[move] = playerVal
#     m = m.reshape(3, 3)
#     m = np.flip(m, flip_axis).flatten()
#     newMove = m.argmax()

#     b = board.reshape(3, 3)
#     newBoard = np.flip(b, flip_axis).flatten()
#     return newBoard, newMove

# log_mirrors = log.copy()
# for item in log:
#     if item[3].agent.name()=='HumanPlayer':
#         b = item[2]
#         m = item[4]
#         pVal = item[3].value
#         for i in [0, 1, [0, 1]]:
#             new_b, new_m = mirror_board(b, m, i, pVal)
#             newItem = item.copy()
#             newItem[2] = new_b
#             newItem[4] = new_m
#             log_mirrors.append(newItem)

cols = ['match', 'move_nr', 'board', 'currPlayer', 'selected_move', 'winner']
data = pd.DataFrame(log, columns=cols)

data['currPlayer_win'] = data.apply(lambda x: True if (x['currPlayer']==x['winner']) else False, axis=1)

match_moves = data.groupby(by=['match'])['move_nr'].max().to_frame('total_moves').reset_index()
data = pd.merge(data, match_moves, on='match')

data['strBoard'] = data['board'].apply(lambda x: ''.join(x.astype(str)))

data['persBoard'] = data.apply(lambda x: x['currPlayer'].value * x['board'], axis=1)
data['strPersBoard'] = data['persBoard'].apply(lambda x: ''.join(x.astype(str)))

data = data[data['currPlayer_win']==True]

# Training data
mask_moves = data['total_moves']<=8
mask_p1 = (data['total_moves']<=5) & (data['currPlayer'].apply(lambda x: x.nr)==1)
mask_p2 = (data['total_moves']<=6) & (data['currPlayer'].apply(lambda x: x.nr)==2)

train_data = data[mask_moves]

data['strPersBoard'].value_counts()

train_data_p1 = data[mask_p1]
train_data_p2 = data[mask_p2]

train_data_p1['total_moves'].value_counts()
train_data_p2['total_moves'].value_counts()

train_cols = ['persBoard', 'selected_move']
# train_data[train_cols].to_pickle(root + r'/data/traindata_rand7moves.pkl.gzip', compression='gzip')
# train_data_p1[train_cols].to_pickle(root + r'/data/traindata_randP1.pkl.gzip', compression='gzip')
# train_data_p2[train_cols].to_pickle(root + r'/data/traindata_randP2.pkl.gzip', compression='gzip')

boards = np.array(list(data['board']))
np.unique(boards, return_counts=True, return_index=True, axis=0)
hash(''.join(boards[2].astype(str)))