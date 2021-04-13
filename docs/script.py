
board = ["X", "X", "X", "O", "", "", "", "O", "X"]

winningPlays = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

def getValueBoard(board):
    lt = []
    for i in board:
        if i=="X":
            lt.append(1)
        elif i=="O":
            lt.append(2)
        else:
            lt.append(0)
    valBoard = [str(x) for x in lt]
    valBoard = ''.join(valBoard)
    return valBoard

def checkWinner(board, winningCombos):
    Xwin = ["X", "X", "X"]
    Owin = ["O", "O", "O"]
    for combination in winningCombos:
        checkWin = [board[i] for i in combination]
        if checkWin==Xwin:
            winner = "X"
            break
        elif checkWin==Owin:
            winner = "O"
            break
        else:
            winner = 0
    return winner

getValueBoard(board)
checkWinner(board, winningPlays)
