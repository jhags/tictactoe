
from browser import document, window, alert

global currPlayer, nextPlayer, currAgent, nextAgent, xAgent, oAgent, winningPlays

xAgent = document["PlayerX-agent"]
xAgent = xAgent.options[xAgent.selectedIndex].value

oAgent = document["PlayerO-agent"]
oAgent = oAgent.options[oAgent.selectedIndex].value

currAgent = xAgent
nextAgent = oAgent

gameStatus = 0

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

def getPlayers():
    xAgent = document["PlayerX-agent"]
    xAgent = xAgent.options[xAgent.selectedIndex].value

    oAgent = document["PlayerO-agent"]
    oAgent = oAgent.options[oAgent.selectedIndex].value

    currAgent = xAgent
    nextAgent = oAgent
    alert(xAgent, oAgent, currAgent, nextAgent)

def newGame():
    global currPlayer, nextPlayer, currAgent, nextAgent

    currPlayer = "O"
    nextPlayer = "X"

    document["C0"].textContent = ""
    document["C1"].textContent = ""
    document["C2"].textContent = ""
    document["C3"].textContent = ""
    document["C4"].textContent = ""
    document["C5"].textContent = ""
    document["C6"].textContent = ""
    document["C7"].textContent = ""
    document["C8"].textContent = ""
    document["game-status"].textContent = ""

    bindAll()
    advanceGame()


def updateCell(cell_ID):
    document[cell_ID].textContent = currPlayer
    document[cell_ID].unbind("click", eval("marker_cell" + str(cell_ID[1])))
    winner = evaluateGame()
    if winner==0:
        advanceGame()

def evaluateGame():
    board = getBoard()
    winner = checkWinner(board, winningPlays)

    if winner!=0:
        if winner!="Draw":
            msg = "Player %s wins!" % winner
        elif winner=="Draw":
            msg = "Draw!"

        unbindAll()
        document["game-status"].textContent = msg

    return winner

def advanceGame():
    changePlayer(currPlayer, nextPlayer, currAgent, nextAgent)
    if currAgent=="1":
        board = getBoard()
        move = botMove(board)
        updateCell(move)


def getBoard():
    board = [
        document["C0"].textContent,
        document["C1"].textContent,
        document["C2"].textContent,
        document["C3"].textContent,
        document["C4"].textContent,
        document["C5"].textContent,
        document["C6"].textContent,
        document["C7"].textContent,
        document["C8"].textContent
    ]
    return board

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
            if "" in board:
                winner = 0
            else:
                winner = "Draw"
    return winner

def changePlayer(current, next, curr_Agent, next_Agent):

    global currPlayer, nextPlayer, currAgent, nextAgent

    temp = current
    current = next
    next = temp

    currPlayer = current
    nextPlayer = next

    temp = curr_Agent
    currAgent = next_Agent
    nextAgent = temp


def getAvailableMoves(board):
    availableMoves = []
    for cell_nr, i in enumerate(board):
        if i=="":
            availableMoves.append(cell_nr)
    return availableMoves

def botMove(board):
    availableMoves = getAvailableMoves(board)
    selectedMove = availableMoves[0]
    cell_ID = "C" + str(selectedMove)
    return cell_ID



def marker_cell0(event):
    updateCell("C0")

def marker_cell1(event):
    updateCell("C1")

def marker_cell2(event):
    updateCell("C2")

def marker_cell3(event):
    updateCell("C3")

def marker_cell4(event):
    updateCell("C4")

def marker_cell5(event):
    updateCell("C5")

def marker_cell6(event):
    updateCell("C6")

def marker_cell7(event):
    updateCell("C7")

def marker_cell8(event):
    updateCell("C8")

def bindAll():
    document["C0"].bind("click", marker_cell0)
    document["C1"].bind("click", marker_cell1)
    document["C2"].bind("click", marker_cell2)
    document["C3"].bind("click", marker_cell3)
    document["C4"].bind("click", marker_cell4)
    document["C5"].bind("click", marker_cell5)
    document["C6"].bind("click", marker_cell6)
    document["C7"].bind("click", marker_cell7)
    document["C8"].bind("click", marker_cell8)

def unbindAll():
    document["C0"].unbind("click", marker_cell0)
    document["C1"].unbind("click", marker_cell1)
    document["C2"].unbind("click", marker_cell2)
    document["C3"].unbind("click", marker_cell3)
    document["C4"].unbind("click", marker_cell4)
    document["C5"].unbind("click", marker_cell5)
    document["C6"].unbind("click", marker_cell6)
    document["C7"].unbind("click", marker_cell7)
    document["C8"].unbind("click", marker_cell8)

def newGameBinding(event):
    newGame()

bindAll()
document["btnNewGame"].bind("click", newGameBinding)
newGame()
getPlayers()
