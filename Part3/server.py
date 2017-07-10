import socket
from collections import deque
import pickle

serverHost = ''
serverPort = 1337
playMsg = 'PLAY'
bufferSize = 1024


def handlePlayRequest(addrset, queue, addr):
        if addr not in addrset:
                queue.append(addr)
                addrset.add(addr)

def getRequest(sock):
        while True:
                try:
                        data, addr = sock.recvfrom(bufferSize)
                except:
                        continue
                msg = pickle.loads(data)
                while msg != playMsg:
                        try:
                                data, addr = sock.recvfrom(bufferSize)
                                msg = pickle.loads(data)
                        except:
                                continue
                return addr
        
def matchPlayers(sock, addrset, queue):
        while len(queue) >= 2:
                addr1 = queue.popleft()
                addr2 = queue.popleft()
                try:
                        sock.sendto(pickle.dumps((addr2, 'O')), addr1)
                        sock.sendto(pickle.dumps((addr1, 'X')), addr2)
                        addrset.remove(addr1)
                        addrset.remove(addr2)
                except:
                        pass

def main():
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind((serverHost, serverPort))
        receivedAddr = set()
        playersQueue = deque()
        while True:
                addr = getRequest(serverSocket)
                handlePlayRequest(receivedAddr, playersQueue, addr)
                matchPlayers(serverSocket, receivedAddr, playersQueue)

if __name__ == '__main__':
        main()
