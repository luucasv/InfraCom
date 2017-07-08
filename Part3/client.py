import pickle
import socket

clientHost = ''
clientPort = 0

serverHost = '' # colocar o ip do servidor aqui (ler quando for rodar?)
serverPort = 1337

def findPlayer(sock):
        

def main():
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.bind((clientHost, clientPort))
        player = findPlayer(clientSocket)

if __name__ == '__main__':
        main()
