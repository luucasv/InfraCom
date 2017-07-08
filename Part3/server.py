import socket
from collections import deque
import pickle

serverHost = ''
serverPort = 1337
playMsg = 'PLAY'
bufferSize = 1024


def handlePlayRequest(IPset, qeue, addr):
        (ip, port) = addr
        if ip not in IPset:
                queue.append(addr) 

def getRequest(sock):
        data, addr = sock.recvfrom(bufferSize)
        while str(data) != playMsg:
                data, addr = sock.recvfrom(bufferSize)
        return addr
        
def matchPlayers(sock, queue):
        while len(queue) >= 2:
                addr1 = queue.popleft()
                addr2 = queue.popleft()
                sock.sendto(pickle.dumps(addr2), addr1)
                sock.sendto(pickle.dumps(addr1), addr2) 

def main():
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind((serverHost, serverPort))
        receivedIPs = set()
        playersQueue = deque()
        while True:
                addr = getRequest(serverSocket)
                handlePlayRequest(receivedIPs, playersQueue, addr)
                matchPlayers(serverSocket, playersQueue)

if __name__ == '__main__':
        main()
