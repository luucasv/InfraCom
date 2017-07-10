import pickle
import socket
import select
import time
from TicTacToe import TicTacToe

# constantes
bufferSize = 1024
clientHost = '' # seu ip
clientPort = 1338
maxSend = 10 # máximo de vezes que a jogada será enviada
maxGet = 10 # máximo de vezes que será verificado o recebimento de uma jogada
maxAck = 10 # máximo de vezes que a socket será verificada na espera de um ack
ack = 'ACK'
waitTime = 5 # tempo em segundos entre as verificações de ack
serverHost = '10.0.0.101' # colocar o ip do servidor aqui (ler quando for rodar?)
serverPort = 1337
playtime = maxGet * waitTime


def findPlayer(sock):
        while True:
                msg = 'PLAY'
                try:
                        sock.sendto(pickle.dumps(msg), (serverHost, serverPort))
                except:
                        raise ConnectionError
                read, _, _ = select.select([sock], [], [], 0)
                for s in read:
                        if s == sock:
                                data, addr = sock.recvfrom(bufferSize)
                                if addr == (serverHost, serverPort):
                                        (player, turn) = pickle.loads(data)
                                        return (player, turn)
                time.sleep(waitTime)

def sendPlay(sock, play, oponent, game, run):
        for i in range(0, maxSend):
                try:
                        sock.sendto(pickle.dumps((play, run)), oponent)
                except:
                        pass
                for j in range(0, maxAck):
                        read, _, _ = select.select([sock], [], [], 0)
                        for s in read:
                                if s == sock:
                                        try:
                                                data, addr = sock.recvfrom(bufferSize)
                                        except:
                                                return False
                                        if addr == oponent:
                                                (msg, r) = pickle.loads(data)
                                                if msg == ack:
                                                        if r == run:
                                                                return True
                                                elif r < run: # old play
                                                        try:
                                                                sock.sendto(pickle.dumps((ack, r)), oponent)
                                                        except:
                                                                pass
                time.sleep(waitTime)
        return False

def getPlay(sock, oponent, game, run):
        for i in range(0, maxGet):
                #print('On try number ' + str(i))
                read, _, _ = select.select([sock], [], [], 0)
                for s in read:
                        if s == sock:
                                try:
                                        data, addr = sock.recvfrom(bufferSize)
                                except:
                                        return False
                                if addr == oponent:
                                        (play, r) = pickle.loads(data)
                                        if r == run and game.makePlay(play[0], play[1]):
                                                try:
                                                        sock.sendto(pickle.dumps((ack, r)), oponent)
                                                except:
                                                        pass
                                                return True
                                        elif r < run: # old play
                                                try:
                                                        sock.sendto(pickle.dumps((ack, r)), oponent)
                                                except:
                                                        pass
                time.sleep(waitTime)
        return False

def handleDisconnect():
        print('Jogo desconectado')

def gameState(sock, turn, oponent):
        game = TicTacToe()
        run = 0
        while game.checkWin() == 'Active':
                if turn == game.getTurn():
                        game.showConsole()
                        print('Aviso: se você demorar mais que %d segundos, poderá ser desconectado. Escolha linha e coluna:'%(playtime))
                        play = input().split()
                        if len(play) == 2 and game.makePlay(play[0], play[1]):
                                received = sendPlay(sock, play, oponent, game, run)
                                if received == False:
                                        handleDisconnect()
                                        return
                                run = run + 1
                        else:
                                print('Jogada invalida!')
                                continue
                else:
                        game.showConsole()
                        print('Esperando por uma jogada')
                        received = getPlay(sock, oponent, game, run)
                        if received == False:
                                handleDisconnect()
                                return
                        run = run + 1
        game.showConsole()
        if game.checkWin() == 'Draw':
                print('O jogo foi um empate!')
        elif game.checkWin() == turn:
                print('Vitoria!')
        else:
                print('Derrota!')


def main():
        while True:
                serverHost = input('Digite o ip do servidor: ')
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                clientSocket.bind((clientHost, clientPort))
                try:
                        (player, turn) = findPlayer(clientSocket)
                except:
                        print('Nao conseguiu estabelecer conexao com o servidor')
                        continue
                gameState(clientSocket, turn, player)
                clientSocket.close()

if __name__ == '__main__':
        main()
