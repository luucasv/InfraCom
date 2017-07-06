import os
import sys
import getpass
from NetworkManager import NetworkManager

class Functions:
	def __getUserInfo(type):
		req = {}
		req['type'] = 'GET_' + type.upper() + '_FOLDER'
		req['login'] = ApplicationManager.userLogin
		req['password'] = ApplicationManager.userPassword
		NetworkManager.sendRequest(req)
		return NetworkManager.recvResponse()['answer']

	def __getItemInfo(type, itemId):
		req = {}
		req['type'] = 'GET_ITEM_' + type.upper()
		req['itemId'] = itemId
		req['login'] = ApplicationManager.userLogin
		req['password'] = ApplicationManager.userPassword
		NetworkManager.sendRequest(req)
		return NetworkManager.recvResponse()['answer']

	def __shareItem(itemId, toLogin):
		req = {}
		req['type'] = 'SHARE_ITEM'
		req['itemId'] = itemId
		req['toLogin'] = toLogin
		req['login'] = ApplicationManager.userLogin
		req['password'] = ApplicationManager.userPassword
		NetworkManager.sendRequest(req)
		response = NetworkManager.recvResponse()
		return str(response['code']) + ' ' + response['status']

	def __authenticate(login, password):
		req = {}
		req['type'] = 'AUTHENTICATE'
		req['login'] = login
		req['password'] = password
		NetworkManager.sendRequest(req)
		return NetworkManager.recvResponse()['status']

	def __regiter(login, password):
		req = {}
		req['type'] = 'REGISTER'
		req['login'] = input('Please enter your login: ')
		req['password'] = getpass.getpass('Please enter your password: ')
		NetworkManager.sendRequest(req)
		response = NetworkManager.recvResponse()
		return str(response['code']) + ' ' + response['status']

	def __creatItem(name, type, where, itemData = ''):
		req = {}
		if type == 'folder':
			req['type'] = 'CREATE_FOLDER'
		else:
			req['type'] = 'CREATE_FILE'
			req['data'] = itemData
		req['where'] = where
		req['name'] = name
		req['login'] = ApplicationManager.userLogin
		req['password'] = ApplicationManager.userPassword
		NetworkManager.sendRequest(req)
		response = NetworkManager.recvResponse()
		return str(response['code']) + ' ' + response['status']

	def __getChildrenMap(currentDirId, currentDirPath):
		currentDirChildren = {}
		if len(currentDirPath) == 0:
			currentDirChildren['home/'] = Functions.__getUserInfo('root')
			currentDirChildren['sharedWithMe/'] = Functions.__getUserInfo('shared')
		else:
			items = Functions.__getItemInfo('data', currentDirId)
			for itemId in items:
				itemName = Functions.__getItemInfo('name', itemId).replace(' ', '_')
				if Functions.__getItemInfo('type', itemId) == 'folder':
					itemName = itemName + '/'
				currentDirChildren[itemName] = itemId
		return currentDirChildren

	def __walkPath(path, remLast, originalDirId, originalDirPath):
		currentDirId = originalDirId
		currentDirPath = originalDirPath[:]

		path = path.strip('/')
		path = path.split('/')
		if path[0] == '~':
			currentDirPath = []
			currentDirId = '0'
			path = path[1:]

		if remLast:
			path = path[:-1]

		for directory in path:
			children = Functions.__getChildrenMap(currentDirId, currentDirPath)
			if directory == '':
				continue

			if directory + '/' in children:
				currentDirId = children[directory + '/']
				currentDirPath.append(directory)
			elif directory == '..' and len(currentDirPath) > 0:
				NetworkManager.sendRequest({'type': 'GET_ITEM_PARENT','itemId': currentDirId, 'login': ApplicationManager.userLogin, 'password': ApplicationManager.userPassword})
				currentDirId = NetworkManager.recvResponse()['answer']
				currentDirPath.pop()
			elif directory != '.':
				return (False, originalDirId, originalDirPath)
		return (True, currentDirId, currentDirPath)

	def __getUnusedName(originalName):
		addOn = ''
		nextId = 1
		while os.path.exists(ApplicationManager.downloadsFolder + '/' + originalName + addOn):
			addOn = '(' + str(nextId) + ')'
			nextId += 1
		return originalName + addOn

	def __saveLocalData(name, data):
		file = open(ApplicationManager.downloadsFolder + '/' + name, 'wb')
		file.write(data)
		file.close()

	def showHelp(args):
		print('Commands:')
		for command, desc in ApplicationManager.commands.items():
			print(command + ' -- ' + desc[0])

	def login(args):
		if ApplicationManager.userLogin != '':
			print('You are already logged in, please logout')
			return

		userLogin = input('Please enter your login: ')
		userPassword = getpass.getpass('Please enter your password: ')
		response = Functions.__authenticate(userLogin, userPassword)

		print(response)
		if response != "Auth OK":
			ApplicationManager.userLogin = ''
			ApplicationManager.userPassword = ''
		else:
			ApplicationManager.userLogin = userLogin
			ApplicationManager.userPassword = userPassword
			ApplicationManager.currentDirPath = []
			ApplicationManager.currentDirId = '0'

	def logout(args):
		ApplicationManager.userLogin = ''
		ApplicationManager.userPassword = ''
		ApplicationManager.currentDirPath = []
		ApplicationManager.currentDirId = '0'

	def register(args):
		if ApplicationManager.userLogin != '':
			print('You are logged in, please logout')
			return

		login = input('Please enter your login: ')
		password = getpass.getpass('Please enter your password: ')
		response = Functions.__regiter(login, password)
		print(response)

	def cd(args):
		if len(args) < 2:
			args.append('~')

		if ApplicationManager.userLogin == '':
			print(args[0] + ': You have to be logged in!')
			return

		ret = Functions.__walkPath(args[1], False, ApplicationManager.currentDirId, ApplicationManager.currentDirPath)
		ApplicationManager.currentDirId = ret[1]
		ApplicationManager.currentDirPath = ret[2]
		if not ret[0]:
			print(args[0] + ': ' + args[1] + ' is not a directory')

	def ls(args):
		if ApplicationManager.userLogin == '':
			print(args[0] + ': You have to be logged in!')
			return

		if len(args) == 1:
			args.append('.')

		ret = Functions.__walkPath(args[1], False, ApplicationManager.currentDirId, ApplicationManager.currentDirPath)
		if ret[0]:
			print(*list(Functions.__getChildrenMap(ret[1], ret[2]).keys()))
		else:
			print(args[0] + ': ' + args[1] + ' is not a directory')

	def mkdir(args):
		if len(args) < 2:
			print(args[0] + ': Missing arguments')
			return

		if ApplicationManager.userLogin == '':
			print(args[0] + ': You have to be logged in!')
			return

		if len(ApplicationManager.currentDirPath) == 0:
			print(args[0] + ': Can\'t create folder here')
			return 

		response = Functions.__creatItem(args[1], 'folder', ApplicationManager.currentDirId)
		print(response)

	def mkfile(args):
		if len(args) < 2:
			print(args[0] + ': Missing arguments')
			return

		if ApplicationManager.userLogin == '':
			print(args[0] + ': You have to be logged in!')
			return

		if len(ApplicationManager.currentDirPath) == 0:
			print(args[0] + ': can\'t create file here')
			return

		if os.path.isfile(args[1]):
			name = os.path.basename(args[1])
			fileData = open(args[1], 'rb').read()
			response = Functions.__creatItem(name, 'file', ApplicationManager.currentDirId, fileData)
			print(response)
		else:
			print(args[0] + ': ' + args[1] + ' is not a file')

	def share(args):
		if len(args) < 3:
			print(args[0] + ': Missing arguments')
			return

		if ApplicationManager.userLogin == '':
			print(args[0] + ': You have to be logged in!')
			return

		item = args[1].strip('/').split('/')[-1]
		add = ''
		if item == '..':
			item = '.'
			add = '/.'
		ret = Functions.__walkPath(args[1] + add, True, ApplicationManager.currentDirId, ApplicationManager.currentDirPath)
		children = Functions.__getChildrenMap(ret[1], ret[2])
		children['.'] = ret[1]
		if item + '/' in children:
			item += '/'
		if ret[0] and item in children:
			response = Functions.__shareItem(children[item], args[2])
			print(response)
		else:
			print(args[0] + ': ' + args[1] + ' is not a file or directory')

	def download(args):
		if len(args) < 2:
			print(args[0] + ': Missing arguments')
			return

		if ApplicationManager.userLogin == '':
			print(args[0] + ': You have to be logged in!')
			return

		ret = Functions.__walkPath(args[1], True, ApplicationManager.currentDirId, ApplicationManager.currentDirPath)
		children = Functions.__getChildrenMap(ret[1], ret[2])
		name = args[1].strip('/').split('/')[-1]
		if ret[0] and name in children:
			data = Functions.__getItemInfo('data', children[name])
			name = Functions.__getUnusedName(name)
			Functions.__saveLocalData(name, data)
			print('File saved in ' + ApplicationManager.downloadsFolder + '/ as ' + name)
		else:
			print(args[0] + ': ' + args[1] + ' is not a file')

	def clear(args):
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')

	def quit(args):
		sys.exit(0)

class ApplicationManager:
	userLogin = ''
	userPassword = ''
	currentDirPath = []
	currentDirId = ''
	downloadsFolder = 'InfraComDrive-Downloads'
	commands = {
		'help': ('show help', Functions.showHelp),
		'login': ('login into your account', Functions.login),
		'logout': ('logout from your account', Functions.logout),
		'register': ('create a new account', Functions.register),
		'cd': ('(cd newdir) move from actual dir to newdir (.. is parent dir)', Functions.cd),
		'ls': ('show all items in the current dir', Functions.ls),
		'mkdir': ('(mkdir dirName) create an empty directory with dirName in the current', Functions.mkdir),
		'mkfile': ('create a file with name and data as the file given as input saved in local storage', Functions.mkfile),
		'share': ('(share itemName userLogin) share an item with an user', Functions.share),
		'download': ('(download fileName) download a file to local storage', Functions.download),
		'clear': ('clear screen', Functions.clear),
		'quit': ('close application', Functions.quit)
	}

	def createDownloadFolder():
		if not os.path.exists(ApplicationManager.downloadsFolder):
			os.mkdir(ApplicationManager.downloadsFolder)

	def printWorkingDir():
		print(ApplicationManager.userLogin + ':' + '/'.join(ApplicationManager.currentDirPath) + '>', end=" ")

	def processCmd(cmd):
		if len(cmd) == 0:
			return
		elif not cmd[0] in ApplicationManager.commands:
			print(cmd[0] + ': command not found')
		else:
			ApplicationManager.commands[cmd[0]][1](cmd)
