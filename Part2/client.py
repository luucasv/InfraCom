import pickle
import socket
import getpass
import sys
import os
import struct

######################### SOCKET STUFF ##############################
bufferSize = 4096
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

def sendRequest(req):
	global sock
	sendMsg(sock, pickle.dumps(req))

def recvResponse():
	global sock
	response = recvMsg(sock)
	return pickle.loads(response)
####################################################################
###################### APPLICATION STUFF ###########################
commands = {}
userLogin = ''
userPassword = ''
currentDirPath = []
currentDirId = ''
currentDirChildren = {}

def showHelp(args):
	print('Commands:')
	for command, desc in commands.items():
		print(command + ' -- ' + desc[0])

def login(args):
	global userLogin
	global userPassword
	global currentDirPath
	global currentDirChildren

	if userLogin != '':
		print('You are already logged in, please logout')
		return
	
	req = {}
	req['type'] = 'AUTHENTICATE'
	req['login'] = input('Please enter your login: ')
	req['password'] = getpass.getpass('Please enter your password: ')
	sendRequest(req)
	response = recvResponse()
	if response['status'] != "Auth OK":
		print(response['status'])
		userLogin = ''
		userPassword = ''
	else:
		userLogin = req['login']
		userPassword = req['password']
		currentDirPath = []
		currentDirChildren = {}
		sendRequest({'type': 'GET_ROOT_FOLDER', 'login': userLogin, 'password': userPassword})
		currentDirChildren['home'] = recvResponse()['answer']
		sendRequest({'type': 'GET_SHARED_FOLDER', 'login': userLogin, 'password': userPassword})
		currentDirChildren['sharedWithMe'] = recvResponse()['answer']

def logout(args):
	global userLogin
	global userPassword
	global currentDirPath

	userLogin = ''
	userPassword = ''
	currentDirPath = []

def register(args):
	global userLogin
	global userPassword
	
	if userLogin != '':
		print('You are logged in, please logout')
		return

	req = {}
	req['type'] = 'REGISTER'
	req['login'] = input('Please enter your login: ')
	req['password'] = getpass.getpass('Please enter your password: ')
	sendRequest(req)
	response = recvResponse()
	print(str(response['code']) + ' ' + response['status'])

def updateCurDir():
	global userLogin
	global userPassword
	global currentDirPath
	global currentDirId
	global currentDirChildren

	if len(currentDirPath) == 0:
		currentDirChildren = {}
		sendRequest({'type': 'GET_ROOT_FOLDER', 'login': userLogin, 'password': userPassword})
		currentDirChildren['home/'] = recvResponse()['answer']
		sendRequest({'type': 'GET_SHARED_FOLDER', 'login': userLogin, 'password': userPassword})
		currentDirChildren['sharedWithMe/'] = recvResponse()['answer']
		return

	req = {}
	req['login'] = userLogin
	req['password'] = userPassword
	req['type'] = 'GET_ITEM_DATA'
	req['itemId'] = currentDirId
	sendRequest(req)
	items = recvResponse()['answer']

	currentDirChildren = {}
	for itemId in items:
		req['type'] = 'GET_ITEM_NAME'
		req['itemId'] = itemId
		sendRequest(req)
		itemName = recvResponse()['answer'].replace(' ', '%20')
		req['type'] = 'GET_ITEM_TYPE'
		sendRequest(req)
		if recvResponse()['answer'] == 'folder':
			itemName = itemName + '/'
		currentDirChildren[itemName] = itemId

def cd(args):
	global userLogin
	global userPassword
	global currentDirPath
	global currentDirId
	global currentDirChildren

	if len(args) < 2:
		args.append('~')

	if userLogin == '':
		print(args[0] + ': You have to be logged in!')
		return

	oldCurrentDirId = currentDirId
	oldCurrentDirPath = currentDirPath

	while args[1][-1] == '/':
		args[1] = args[1][:-1]

	path = args[1].split('/')
	if path[0] == '~':
		currentDirPath = []
		currentDirId = '0'
		path = path[1:]

	for directory in path:
		updateCurDir()
		if directory + '/' in currentDirChildren:
			directory = directory + '/'
		elif directory[-1] != '/' and directory != '..' and directory != '.':
			print(args[0] + ': ' + args[1] + ' is not a directory')
			currentDirId = oldCurrentDirId
			currentDirPath = oldCurrentDirPath
			return

		if directory in currentDirChildren:
			currentDirId = currentDirChildren[directory]
			currentDirPath.append(directory[:-1])
		elif directory == '..' and len(currentDirPath) > 0:
			sendRequest({'type': 'GET_ITEM_PARENT','itemId': currentDirId, 'login': userLogin, 'password': userPassword})
			currentDirId = recvResponse()['answer']
			currentDirPath.pop()
		elif directory != '.':
			print(args[0] + ": Directory " + args[1] + " does not exist")
			currentDirId = oldCurrentDirId
			currentDirPath = oldCurrentDirPath
			return

def ls(args):
	global userLogin
	global userPassword
	global currentDirPath
	global currentDirId
	global currentDirChildren

	if userLogin == '':
		print(args[0] + ': You have to be logged in!')
		return

	updateCurDir()

	print(*list(currentDirChildren.keys()))

def mkdir(args):
	global userLogin
	global userPassword
	global currentDirId
	global currentDirPath

	if len(args) < 2:
		print(args[0] + ': Missing arguments')
		return

	if userLogin == '':
		print(args[0] + ': You have to be logged in!')
		return

	if len(currentDirPath) == 0:
		print(args[0] + ': Can\'t create folder here')
		return 

	req = {'login': userLogin, 'password': userPassword, 'type': 'CREATE_FOLDER', 'where': currentDirId, 'name': args[1]}
	sendRequest(req)
	res = recvResponse()
	print(str(res['code']) + ' ' + res['status'])

def mkfile(args):
	global userLogin
	global userPassword
	global currentDirId
	global currentDirPath

	if len(args) < 2:
		print(args[0] + ': Missing arguments')
		return

	if userLogin == '':
		print(args[0] + ': You have to be logged in!')
		return

	if len(currentDirPath) == 0:
		print(args[0] + ': can\'t create file here')
		return

	if os.path.isfile(args[1]):
		name = os.path.basename(args[1])
		fileData = open(args[1], 'rb').read()
		sendRequest({'type': 'CREATE_FILE', 'where': currentDirId, 'name': name, 'data': fileData, 'login': userLogin, 'password': userPassword})
		res = recvResponse()
		print(str(res['code']) + ' ' + res['status'])
	else:
		print(args[1] + ' nao eh file')


def clear(args):
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

def quit(args):
	sys.exit(0)

commands = {
	'help': ('show help', showHelp),
	'login': ('login into your account', login),
	'logout': ('logout from your account', logout),
	'register': ('create a new account', register),
	'cd': ('(cd newdir) move from actual dir to newdir (.. is parent dir)', cd),
	'ls': ('show all items in the current dir', ls),
	'mkdir': ('(mkdir dirName) create an empty directory with dirName in the current', mkdir),
	'mkfile': ('create a file with name and data as the file given as input saved in local storage', mkfile),
	'clear': ('clear screen', clear),
	'quit': ('close application', quit)
}
####################################################################
def main():
	if len(sys.argv) != 3:
		print ('Usage : python3 client.py hostname port')
		sys.exit(1)

	host = sys.argv[1]
	port = int(sys.argv[2])
	 
	sock.settimeout(None)
	 
	try :
		sock.connect((host, port))
	except :
		print('Unable to connect. Maybe the server is not up.')
		sys.exit()

	print('Welcome to file system betha 1.0.0')
	while True:
		print(userLogin + ':' + '/'.join(currentDirPath) + '>', end=" ")
		cmd = input().split()

		if not cmd[0] in commands:
			print(cmd[0] + ': command not found')
		else:
			commands[cmd[0]][1](cmd)

if __name__ == '__main__':
	main()