

const selectPlayers = () => {
    player_text = document.getElementById("btnPlayers").textContent

    PvC = "Human vs Computer"
    CvP = "Computer vs Human"
    human = "human"
    computer = "computer"
    P1marker = "X"
    P2marker = "O"

    if (player_text==PvC) {
        P1agent = human
        P2agent = computer
    } else if (player_text==CvP) {
        P1agent = computer
        P2agent = human
    }

    match = [
        [P1agent, P1marker],
        [P2agent, P2marker]
    ]

    return match
}


function changePlayers() {
    [Game.currPlayer, Game.nextPlayer] = [Game.nextPlayer, Game.currPlayer]
}


const checkWinner = () => {
    Xwin = ["X", "X", "X"]
    Owin = ["O", "O", "O"]

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

    for (const winningPlay of winningPlays) {
        checkWin = []
        for (const i of winningPlay) {
            checkWin.push(Game.board[i])
        }

        if (checkWin.join()==Xwin.join()) {
            Game.winner = "X"
            Game.msg = "Player X wins!"
            deactivateBoard()
            return

        } else if (checkWin.join()==Owin.join()) {
            Game.winner = "O"
            Game.msg = "Player O wins!"
            deactivateBoard()
            return

        } else {
            if (Game.board.includes("")) {
                // continue
            } else {
                Game.winner = "Draw"
                Game.msg = "Draw!"
            }
        }
    }
}


function convertBoard(iconBoard) {
    hashBoard = ''
    for (const cell of iconBoard) {
        if (cell=="X") {
            hashBoard += "1"
        } else if (cell=="O") {
            hashBoard += "2"
        } else {
            hashBoard += "0"
        }
    }
    return hashBoard
}


async function getComputerMove() {
    hashBoard = convertBoard(Game.board)
    delay = 750
    url = `https://noughtsandcrosses.azurewebsites.net/api/noughts-and-crosses?code=zrXeaclgRR2X/1smIaojuDyT8u5hWSwyi4WD0HRyBwmm6/zSOePAaQ==&board=${hashBoard}&player_turn=${Game.currPlayer[1]}&delay=${delay}`

    const request = async () => {
        const response = await fetch(url)
        const data = await response.json()
        // console.log(data)

        return data
    }

    jsondata = await request()
    let cellID = "C" + jsondata.selected_move

    playerMove(cellID)
}


function playerMove(selectedCell) {
    cellNr = parseInt(selectedCell.charAt(1))
    Game.board[cellNr] = Game.currPlayer[1]

    updateBoard(selectedCell)
    checkWinner()
    playerMessage()
    changePlayers()

    if ((Game.currPlayer[0]=="computer") && (Game.winner==null)) {
        getComputerMove()
    }

}


function playerMessage() {
    elemGameStatus = document.getElementById("game-status")
    elemXline = document.getElementById("Xplayer-underling")
    elemOline = document.getElementById("Oplayer-underling")
    if (Game.winner==null) {
        elemGameStatus.textContent = `Player ${Game.nextPlayer[1]} to move`
        if (Game.nextPlayer[1]=="X") {
            elemXline.style.display = "block"
            elemOline.style.display = "none"
        } else {
            elemXline.style.display = "none"
            elemOline.style.display = "block"
        }
    } else {
        elemGameStatus.textContent = Game.msg
    }
}


function updateBoard(selected_cell) {
    elem = document.getElementById(selected_cell)
    elem.innerHTML = Game.currPlayer[1]
    elem.style.pointerEvents = 'none'
}


function clickChooseMatch() {
    let PvC = "Human vs Computer"
    let CvP = "Computer vs Human"

    elem = document.getElementById("btnPlayers")
    btnPlayerText = elem.textContent

    if (btnPlayerText==PvC) {
        elem.innerHTML = CvP
    } else if (btnPlayerText==CvP) {
        elem.innerHTML = PvC
    }
}


function resetBoard() {
    cells = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
    for (const cell of cells) {
        elem = document.getElementById(cell)
        elem.textContent = ""
        elem.style.pointerEvents = 'auto'
    }

    document.getElementById("game-status").textContent = ""
}


function deactivateBoard() {
    cells = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
    for (const cell of cells) {
        elem = document.getElementById(cell)
        elem.style.pointerEvents = 'none'
    }
    document.getElementById("btnNewGame").innerHTML = "Play again?"
}


function startNewGame() {
    document.getElementById("btnNewGame").innerHTML = "Restart"

    Game = {
        match: selectPlayers(),
        currPlayer: this.match[0],
        nextPlayer: this.match[1],
        board: ["", "", "", "", "", "", "", "", ""],
        winner: null,
        msg: null
    }

    resetBoard()

    if ((Game.currPlayer[0]=="computer") && (Game.winner==null)) {
        getComputerMove()
    }

}
