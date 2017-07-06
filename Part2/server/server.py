import threading
import socket
import pickle
import struct
from RequestManager import RequestManager

requestManager = RequestManager()
requestManagerLock = threading.Lock()
bufferSize = 4096
host = ''
port = 20041

def sendMsg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recvMsg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''.encode()
    while len(data) < n:
        packet = sock.recv(min(n - len(data), bufferSize))
        if not packet:
            return None
        data += packet
    return data


def handleClient(newSock, addr):
	while True:
		request = recvMsg(newSock)
		if not request:
			print('Client at ' + str(addr) + ' logged out!')
			return
		else:
			request = pickle.loads(request)
			requestManagerLock.acquire()
			response = requestManager.processRequest(request)
			requestManagerLock.release()
			sendMsg(newSock, pickle.dumps(response))

def main():
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
	serverSocket.bind((host, port))
	serverSocket.listen(10)

	print("Part2 server up! " + str(serverSocket.getsockname()))
	while True:
		newSock, addr = serverSocket.accept()
		print("New Client with addr = " + str(addr))                
		newClient = threading.Thread(target = handleClient, args = (newSock, addr))
		newClient.start()
                


if __name__ == '__main__':
	main()