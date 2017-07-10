class TicTacToe:
        def __init__(self):
                self.__board = [['.' for x in range(3)] for y in range(3)]
                self.__curPlayer = 'O'
                self.__rounds = 0

        def makePlay(self, x, y):
                try:
                        x = int(x)
                        y = int(y)
                except ValueError:
                        return False
                if x < 0 or x >= 3 or y < 0 or y >= 3:
                        return False
                if self.checkWin() != 'Active':
                        return False
                if not self.__board[x][y] == '.':
                        return False
                self.__board[x][y] = self.__curPlayer
                if self.__curPlayer == 'O':
                        self.__curPlayer = 'X'
                else:
                        self.__curPlayer = 'O'
                self.__rounds = self.__rounds + 1
                return True

        def __checkWin(self, player):
                for i in range(3):
                        win = True
                        for j in range(3):
                                if not self.__board[i][j] == player:
                                        win = False
                        if win:
                                return True
                        win = True
                        for j in range(3):
                                if not self.__board[j][i] == player:
                                        win = False
                        if win:
                                return True
                win = True
                for i in range(3):
                        if not self.__board[i][i] == player:
                                win = False
                if win:
                        return True
                win = True
                for i in range(3):
                        if not self.__board[2 - i][i] == player:
                                win = False
                return win

        def checkWin(self):
                if self.__checkWin('O'):
                        return 'O'
                elif self.__checkWin('X'):
                        return 'X'
                elif self.__rounds == 9:
                        return 'Draw'
                else:
                        return 'Active'

        def showConsole(self):
                for i in range(3):
                        print(self.__board[i][0] + ' ' + self.__board[i][1] + ' ' + self.__board[i][2])

        def getTurn(self):
                return self.__curPlayer

def main():
        while True:
                game = TicTacToe()
                while game.checkWin() == 'Active':
                        game.showConsole()
                        print('Status: ' + game.checkWin() + ' Turn of player ' + game.getTurn())
                        print('Escolha linha e coluna:')
                        a = input().split()
                        if len(a) == 2 and game.makePlay(a[0], a[1]):
                                game.makePlay(a[0], a[1])
                        else:
                                print('Jogada invalida')
                print('Game has ended!')
                if game.checkWin() == 'Draw':
                        print('It was a Draw!')
                else:
                        print(game.checkWin() + ' has won!')


if __name__ == '__main__':
        main()
