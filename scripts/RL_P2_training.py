''' Play trained model '''
import os
import sys

import pandas as pd
import numpy as np

from comet_ml import Experiment

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe import BotPlayer, Game, HumanPlayer, RandomPlayer, simulate

    # Add the following code anywhere in your machine learning file
experiment = Experiment(api_key="",
                    project_name="noughts-and-crosses", workspace="jhags",
                    auto_param_logging=False,
                    log_code=False, auto_output_logging=False,
                    log_env_details=False, log_env_cpu=False, log_env_gpu=False,
                    log_env_host=False, display_summary_level=0)

experiment_tag = "Player2"
rewards = [3, 1, -10]
learningRate = 0.1
discount = 0.6
games = 25000
epsilon = 0.4
test_batch = 100

lineup = [
    # (BotPlayer(player1=True, greedy_epsilon=0.4), RandomPlayer()),
    (RandomPlayer(), BotPlayer(player1=False, greedy_epsilon=epsilon)),
]

log = []
for match in lineup:
    P1 = match[0]
    P2 = match[1]

    print(P1.name() + ' vs ' + P2.name())

    for game_nr in range(games):
        game = Game(P1, P2)
        game.play(print_board=False, record_history=True)

        P2.update_model(game, rewards, learningRate, discount)

        if (game_nr+1)%test_batch==0:
            model_test = simulate([RandomPlayer(), BotPlayer(model=P2.model)], test_batch)
            log.append((game_nr+1,) + model_test)

P2.save_model(root + r'/model/P2model.json')

experiment.add_tag(experiment_tag)

# Log metrics
experiment.log_metrics({
    "win_reward": rewards[0],
    "draw_reward": rewards[1],
    "lose_reward": rewards[2],
    "learning_rate": learningRate,
    "discount": discount,
    "training_games": games,
    "greedy_epsilon": epsilon,
    "test_batch": test_batch
})


# nr training games, win, draw, lost
for step, (g, w, d, l) in enumerate(log):
    # print(step, g, w, d, l)
    experiment.log_metric('training_games', g, step=g, epoch=step)
    experiment.log_metric('P1_win', w, step=g, epoch=step)
    experiment.log_metric('P1_draw', d, step=g, epoch=step)
    experiment.log_metric('P1_lost', l, step=g, epoch=step)

experiment.end()
