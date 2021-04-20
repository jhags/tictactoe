import logging
import json
import azure.functions as func

from . import game


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    board = req.params.get('board')
    player_turn = req.params.get('player_turn')
    difficulty = req.params.get('difficulty')

    if not player_turn:
        player_turn = 'X'

    if not difficulty:
        difficulty = 'hard'

    selected_move = game.select_move(board, player_turn=player_turn, difficulty=difficulty)

    response = {
        'inputs': {
            'board': board,
            'player_turn': player_turn,
            'difficulty': difficulty
        },
        'selected_move': selected_move
    }

    return func.HttpResponse(
        body=json.dumps(response),
        status_code=200,
        mimetype="application/json")
