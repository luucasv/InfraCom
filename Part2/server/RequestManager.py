from SystemManager import SystemManager

class Messages:
	invalidRequest = {
		'status': 'Error', 
		'code': 404, 
		'answer': 'Invalid Request'
	}
	loginExists = {
		'status': 'Error',
		'code': 401,
		'answer': 'Login already exists'
	}
	invalidLoginOrPassWord = {
		'status': 'Error',
		'code': 402,
		'answer': 'Invalid login or password'
	}
	getError = {
		'status': 'Error',
		'code': 403,
		'answer': 'File or directory doesnt exist'
	}
	getOK = {
		'status': 'Success',
		'code': 200
	}
	userCreated = {
		'status': 'Success',
		'code': 201,
		'answer': 'User created'
	}
	permissionGiven = {
		'status': 'Success',
		'code': 202,
		'answer': 'Permission given'
	}
	itemRenamed = {
		'status': 'Success',
		'code': 203,
		'answer': 'Item renamed'
	}
	itemMoved = {
		'status': 'Success',
		'code': 204,
		'answer': 'Item moved'
	}
	fileEdited = {
		'status': 'Success',
		'code': 205,
		'answer': 'File edited'
	}
	authOk = {
		'status': 'Success',
		'code': 206,
		'answer': 'Successfull authentication'
	}
	folderCreated = {
		'status': 'Success',
		'code': 207,
		'answer': 'Folder Created'
	}
	fileCreated = {
		'status': 'Success',
		'code': 208,
		'answer': 'File Created'
	}

class RequestManager:
	def __init__(self):
		self.__systemManager = SystemManager()

	def processRequest(self, request):
		if not type(request) is dict:
			return Messages.invalidRequest

		elif not 'type' in request:
			return Messages.invalidRequest
		
		elif not 'login' in request or not 'password' in request:
			return Messages.invalidRequest
		
		elif request['type'] == 'REGISTER':
			if not self.__systemManager.createClient(request['login'], request['password']):
				return Messages.loginExists
			else:
				return Messages.userCreated
		
		elif not self.__systemManager.authenticate(request['login'], request['password']):
			return Messages.invalidLoginOrPassWord
		
		elif request['type'] == 'AUTHENTICATE':
			return Messages.authOk
		
		elif request['type'].startswith('GET_ITEM'):
			if not 'itemId' in request:
				return Messages.invalidRequest
			answer = False
			if request['type'] == 'GET_ITEM_NAME':
				answer = self.__systemManager.getItemName(request['login'], request['itemId'])
			elif request['type'] == 'GET_ITEM_DATA':
				answer = self.__systemManager.getItemData(request['login'], request['itemId'])
			elif request['type'] == 'GET_ITEM_TYPE':
				answer = self.__systemManager.getItemType(request['login'], request['itemId'])
			elif request['type'] == 'GET_ITEM_PARENT':
				answer = self.__systemManager.getItemParentId(request['login'], request['itemId'])
			if type(answer) is bool and not answer:
				return Messages.getError
			else:
				return dict(Messages.getOK, **{'answer': answer})

		elif request['type'] == 'CREATE_FOLDER':
			if not 'where' in request:
				return Messages.invalidRequest
			if not 'name' in request:
				return Messages.invalidRequest
			createdId = self.__systemManager.createFolder(request['login'], request['name'], request['where'])
			if type(createdId) is bool and not createdId:
				return Messages.invalidRequest
			return Messages.folderCreated

		elif request['type'] == 'CREATE_FILE':
			if not 'where' in request:
				return Messages.invalidRequest
			if not 'name' in request:
				return Messages.invalidRequest
			if not 'data' in request:
				return Messages.invalidRequest
			createdId = self.__systemManager.createFile(request['login'], request['name'], request['data'], request['where'])
			if type(createdId) is bool and not createdId:
				return Messages.invalidRequest
			return Messages.fileCreated
		
		elif request['type'] == 'GET_ROOT_FOLDER':
			client = self.__systemManager.getClient(request['login'])
			return dict(Messages.getOK, **{'answer': client.getRootFolder()})
		
		elif request['type'] == 'GET_SHARED_FOLDER':
			client = self.__systemManager.getClient(request['login'])
			return dict(Messages.getOK, **{'answer': client.getSharedFolder()})
		
		elif request['type'] == 'SHARE_ITEM':
			if not 'itemId' in request or not 'toLogin' in request:
				return Messages.invalidRequest
			if not self.__systemManager.addPermission(request['itemId'], request['login'], request['toLogin']):
				return Messages.invalidRequest
			else:
				return Messages.permissionGiven
		
		elif request['type'] == 'RENAME_ITEM':
			if not 'itemId' in request or not 'newName' in request:
				return Messages.invalidRequest
			if not self.__systemManager.renameItem(request['login'], request['itemId'], request['newName']):
				return Messages.invalidRequest
			else:
				return Messages.itemRenamed
		
		elif request['type'] == 'EDIT_FILE_DATA':
			if not 'fileId' in request or not 'newData' in request:
				return Messages.invalidRequest
			if not self.__systemManager.editFileData(request['login'], request['fileId'], request['newData']):
				return Messages.invalidRequest
			else:
				return Messages.fileEdited
		
		elif request['type'] == 'MOVE_ITEM':
			if not 'itemId' in request or not 'newParent' in request:
				return Messages.invalidRequest
			if not self.__systemManager.moveItem(request['login'], request['itemId'], request['newParent']):
				return Messages.invalidRequest
			else:
				return Messages.itemMoved
		
		else:
			return Messages.invalidRequest

def getReq():
	req = {}
	req['type'] = input()
	req['login'] = input()
	req['password'] = input()
	if req['type'].startswith('GET_ITEM'):
		req['itemId'] = input()
	elif req['type'] == 'CREATE_FILE':
		req['where'] = input()
		req['name'] = input()
		req['data'] = input()
	elif req['type'] == 'CREATE_FOLDER':
		req['where'] = input()
		req['name'] = input()
	elif req['type'] == 'SHARE_ITEM':
		req['itemId'] = input()
		req['toLogin'] = input()
	elif req['type'] == 'RENAME_ITEM':
		req['itemId'] = input()
		req['newName'] = input()
	elif req['type'] == 'MOVE_ITEM':
		req['itemId'] = input()
		req['newParent'] = input()
	elif req['type'] == 'EDIT_FILE_DATA':
		req['itemId'] = input()
		req['newData'] = input()
	return req

if __name__ == '__main__':
	rm = Messages()
	while True:
		req = getReq()
		res = rm.processRequest(req)
		print(str(res))
