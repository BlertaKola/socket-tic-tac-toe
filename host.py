

import socket

class TicTacToe:

    def __init__(self):
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.game_over = False
        self.counter = 0

    def start_game(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 9999))
        server.listen(1)

        print("Waiting for a connection...")
        client, addr = server.accept()
        print("Connected!")

        while not self.game_over:
            if self.turn == self.you:
                move = self.get_user_move()
                client.send(','.join(move).encode('utf-8'))
                self.apply_move(move, self.you)
                self.turn = self.opponent
            else:
                data = client.recv(1024).decode('utf-8')
                if not data:
                    break
                move = data.split(',')
                self.apply_move(move, self.opponent)
                self.turn = self.you

        client.close()
        server.close()

    def get_user_move(self):
        move = input("Enter a move in the format (row,column): ")
        return move.split(',')

    def apply_move(self, move, player):
        if self.game_over:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        if self.check_if_won():
            if self.winner == self.you:
                print("You win!")
            elif self.winner == self.opponent:
                print("You lose!")
        elif self.counter == 9:
            print("It is a tie!")

    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                self.winner = self.board[0][col]
                self.game_over = True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.winner = self.board[0][2]
            self.game_over = True
            return True
        return False

    def print_board(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("-------------")

if __name__ == "__main__":
    game = TicTacToe()
    game.start_game()
