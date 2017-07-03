import pickle
import socket
import getpass
import sys

bufferSize = 4096

def getReq():
	req = {}
	req['type'] = input('Please enter the request type: ')
	req['login'] = input('Please enter your login: ')
	req['password'] = getpass.getpass('Please enter your password: ')
	if req['type'].startswith('GET_ITEM'):
		req['itemId'] = input('Please enter the item id: ')
	elif req['type'] == 'CREATE_FILE':
		req['where'] = input('Please enter the folder you want to create the file: ')
		req['name'] = input('Please enter the file name: ')
		req['data'] = input('Please enter the file data: ')
	elif req['type'] == 'CREATE_FOLDER':
		req['where'] = input('Please enter the folder you want to create the folder: ')
		req['name'] = input('Please enter the folder name: ')
	elif req['type'] == 'SHARE_ITEM':
		req['itemId'] = input('Please enter the item id: ')
		req['toLogin'] = input('Please enter the login you want to share with: ')
	elif req['type'] == 'RENAME_ITEM':
		req['itemId'] = input('Please enter the item id: ')
		req['newName'] = input('Please enter the new name: ')
	elif req['type'] == 'MOVE_ITEM':
		req['itemId'] = input('Please enter the item id: ')
		req['newParent'] = input('Please enter the id where you want to move to: ')
	elif req['type'] == 'EDIT_FILE_DATA':
		req['itemId'] = input('Please enter the item id: ')
		req['newData'] = input('Please enter the new data: ')
	return req

def sendRequest(sock, req):
	sock.sendall(pickle.dumps(req))

def recvResponse(sock):
	response = sock.recv(bufferSize)
	return pickle.loads(response)

def main():
	if len(sys.argv) != 3:
		print ('Usage : python3 client.py hostname port')
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])
	 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(None)
	 
	try :
		sock.connect((host, port))
	except :
		print('Unable to connect. Maybe the server is not up.')
		sys.exit()

	print('Welcome to file system betha 1.0.0')
	while True:
		print('=' * 100)
		req = getReq()
		print('Your request: ' + str(req))
		sendRequest(sock, req)
		print('Response: ' + str(recvResponse(sock)))
		print('=' * 100)

if __name__ == '__main__':
	main()