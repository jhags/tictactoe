from game import Game


xPlayer = 1
oPlayer = -1

game = Game('new')
game.print_board()

while game.status == 0:
    game.player_routine(xPlayer)
    game.print_board()

    game.player_routine(oPlayer)
    game.print_board()