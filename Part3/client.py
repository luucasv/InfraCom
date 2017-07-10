import pickle
import socket
import select
from TicTacToe import TicTacToe
from time import sleep

# constantes
bufferSize = 1024
clientHost = '' # seu ip
clientPort = 1337
maxSend = 10 # máximo de vezes que a jogada será enviada
maxGet = 10 # máximo de vezes que será verificado o recebimento de uma jogada
maxAck = 10 # máximo de vezes que a socket será verificada na espera de um ack
ack = 'ACK'
waitTime = 5 # tempo em segundos entre as verificações de ack
serverHost = '10.0.0.105' # colocar o ip do servidor aqui (ler quando for rodar?)
serverPort = 1337
playtime = maxGet * waitTime


def findPlayer(sock):
        while True:
                msg = 'PLAY'
                sock.sendto(pickle.dumps(msg), (serverHost, serverPort))
                read, _, _ = select.select([sock], [], [])
                for s in read:
                        if s == sock:
                                data, addr = sock.recvfrom(bufferSize)
                                if addr == (serverHost, serverPort):
                                        (player, turn) = pickle.loads(data)
                                        return (player, turn)
                time.sleep(waitTime)

def sendPlay(sock, play, oponent, game, run):
        for i in range(0, maxSend):
                sock.sendto(pickle.dumps((play, run)), oponent)
                for j in range(0, maxAck):
                        read, _, _ = select.select([sock], [], [])
                        for s in read:
                                if s == sock:
                                        data, addr = sock.recvfrom(bufferSize)
                                        if addr == oponent:
                                                (msg, r) = pickle.loads(data)
                                                if msg == ack:
                                                        if r == run:
                                                                return True
                                                elif r < run: # old play
                                                        sock.sendto(pickle.dumps((ack, r)), oponent)
                time.sleep(waitTime)
        return False

def getPlay(sock, oponent, game, run):
        for i in range(0, maxGet):
                read, _, _ = selec.select([sock], [], [])
                for s in read:
                        if s == sock:
                                data, addr = sock.recvfrom(bufferSize)
                                if addr == oponent:
                                        (play, r) = pickle.loads(data)
                                        if r == run and game.makePlay(play[0], play[1]):
                                                sock.sendto(pickle.dumps((ack, r)), oponent)
                                                return True
                                        elif r < run: # old play 
                                                sock.sendto(pickle.dumps((ack, r)), oponent)
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
                        print('Esperando por uma jogada')
                        received = getPlay(sock, oponent, game, run)
                        if received == False:
                                handleDisconnect()
                                return
                        run = run + 1
        if game.checkWin() == 'Draw':
                print('O jogo foi um empate!')
        elif game.checkWin() == turn:
                print('Vitoria!')
        else:
                print('Derrota!')


def main():
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.bind((clientHost, clientPort))
        (player, turn) = findPlayer(clientSocket)
        while True:
            gameState(clientSocket, turn, (serverHost, serverPort))

if __name__ == '__main__':
        main()
