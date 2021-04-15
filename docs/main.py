
from browser import document, window, alert


class newGame():

    def __init__(self):
        self.match = self.selectPlayers()
        self.currPlayer = self.match[0]
        self.nextPlayer = self.match[1]
        self.board = ["", "", "", "", "", "", "", "", ""]
        self.reset_board()
        self.winner = "none"
        self.bind_all()
        self.winning_plays = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        if self.currPlayer[0]=="computer":
            self.move_bot()


    def player_move(self, selected_cell):
        # update game
        cell_nr = int(selected_cell[1])
        self.board[cell_nr] = self.currPlayer[1]

        # Print icon to borad
        document[selected_cell].textContent = self.currPlayer[1]

        # unbind cell
        document[selected_cell].unbind("click", event_cell)

       # Check for a winner
        self.checkWinner()

        # Update player turn message
        self.player_message()

        # swap players
        self.change_players()

        # Computer move
        if (self.currPlayer[0]=="computer") and (self.winner=="none"):
            self.move_bot()


    def selectPlayers(self):
        player_text = document["btnPlayers"].text

        PvC = "Human vs Computer"
        CvP = "Computer vs Human"
        human, computer = "human", "computer"
        P1marker, P2marker = "X", "O"

        if player_text==PvC:
            P1agent, P2agent = human, computer

        elif player_text==CvP:
            P1agent, P2agent = computer, human

        match = [
            [P1agent, P1marker],
            [P2agent, P2marker]
        ]

        return match


    def change_players(self):
        self.currPlayer, self.nextPlayer = self.nextPlayer, self.currPlayer

    def player_message(self):
        if self.winner=="none":
            document["game-status"].textContent = "Player %s to move" % self.nextPlayer[1]
            if self.currPlayer[0]=="X":
                document["Xplayer-underling"].style.display = "block"
                document["Oplayer-underling"].style.display = "none"
            else:
                document["Xplayer-underling"].style.display = "block"
                document["Oplayer-underling"].style.display = "none"

    def checkWinner(self):
        Xwin = ["X", "X", "X"]
        Owin = ["O", "O", "O"]

        for combination in self.winning_plays:

            checkWin = [self.board[i] for i in combination]

            if checkWin==Xwin:
                self.winner = "X"
                msg = "Player X wins!"
                break

            elif checkWin==Owin:
                self.winner = "O"
                msg = "Player O wins!"
                break

            else:
                if "" in self.board:
                    self.winner = "none"
                else:
                    self.winner = "Draw"
                    msg = "Draw!"

        if self.winner=="none":
            pass
        else:
            document["game-status"].textContent = msg
            self.unbind_all()


    def get_computer_move(self):

        availableMoves = []
        for idx, val in enumerate(self.board):
            if val=="":
                availableMoves.append(idx)

        selectedMove = availableMoves[0]
        cell_ID = "C" + str(selectedMove)
        return cell_ID


    def move_bot(self):
        bot_cell = self.get_computer_move()
        self.player_move(bot_cell)


    def reset_board(self):
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

    def bind_all(self):
        for i in range(9):
            document["C" + str(i)].bind("click", event_cell)

    def unbind_all(self):
        for i in range(9):
            document["C" + str(i)].unbind("click", event_cell)

# Event fns

def event_cell(event):
    selected_cell = event.currentTarget.id
    game.player_move(selected_cell)


def click_selectPlayers(event):
    PvC = "Human vs Computer"
    CvP = "Computer vs Human"

    player_text = document["btnPlayers"].text

    if player_text==PvC:
        document["btnPlayers"].textContent = CvP

    elif player_text==CvP:
        document["btnPlayers"].textContent = PvC


def click_newGame(event):
    global game
    game = newGame()

document["btnPlayers"].bind("click", click_selectPlayers)
document["btnNewGame"].bind("click", click_newGame)

