import socket
import pickle
import struct

class NetworkManager:
	bufferSize = 4096
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __sendMsg(msg):
	    msg = struct.pack('>I', len(msg)) + msg
	    NetworkManager.sock.sendall(msg)

	def __recvMsg():
	    raw_msglen = NetworkManager.__recvall(4)
	    if not raw_msglen:
	        return None
	    msglen = struct.unpack('>I', raw_msglen)[0]
	    return NetworkManager.__recvall(msglen)

	def __recvall(n):
	    data = ''.encode()
	    while len(data) < n:
	        packet = NetworkManager.sock.recv(min(n - len(data), NetworkManager.bufferSize))
	        if not packet:
	            return None
	        data += packet
	    return data

	def sendRequest(req):
		NetworkManager.__sendMsg(pickle.dumps(req))

	def recvResponse():
		response = NetworkManager.__recvMsg()
		return pickle.loads(response)

	def connect(pair):
		NetworkManager.sock.settimeout(None)
		NetworkManager.sock.connect(pair)
		