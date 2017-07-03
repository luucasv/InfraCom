import threading
import socket
import pickle
from RequestManager import RequestManager

requestManager = RequestManager()
requestManagerLock = threading.Lock()
bufferSize = 4096
host = ''
port = 20041

def handleClient(newSock, addr):
	while True:
		request = newSock.recv(bufferSize)
		if not request:
			print('Client at ' + str(addr) + ' logged out!')
			return
		else:
			request = pickle.loads(request)
			requestManagerLock.acquire()
			response = requestManager.processRequest(request)
			requestManagerLock.release()
			newSock.sendall(pickle.dumps(response))

def main():
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
	serverSocket.bind((host, port))
	serverSocket.listen(10)

	print("Part2 server up!")
	while True:
		newSock, addr = serverSocket.accept()
		print("New Client with addr = " + str(addr))                
		newClient = threading.Thread(target = handleClient, args = (newSock, addr))
		newClient.start()
                


if __name__ == '__main__':
	main()