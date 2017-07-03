from SystemManager import SystemManager

class RequestManager:
	__invalidRequest = {"status": "Invalid request", "code": 404}
	__loginExists = {"status": "Login already exists", "code": 401}
	__userCreated = {"status": "Register OK", "code": 201, "answer": "User created"}
	__invalidLogin = {"status": "Invalid login or password", "code": 400}
	__permissionGiven = {"status": "Permission OK", "code": 202, "answer": "Permission given"}
	__itemRenamed = {"status": "Rename OK", "code": 203, "answer": "Item renamed"}
	__itemMoved = {"status": "Move OK", "code": 204, "answer": "Item moved"}
	__fileEdited = {"status": "Edit OK", "code": 205, "answer": "File edited"}
	def __init__(self):
		self.__systemManager = SystemManager()

	def processRequest(self, request):
		if not type(request) is dict:
			return RequestManager.__invalidRequest
		elif not "type" in request:
			return RequestManager.__invalidRequest
		elif not "login" in request or not "password" in request:
			return RequestManager.__invalidRequest
		elif request['type'] == "REGISTER":
			if not self.__systemManager.createClient(request['login'], request['password']):
				return RequestManager.__loginExists
			else:
				return RequestManager.__userCreated
		elif not self.__systemManager.authenticate(request['login'], request['password']):
			return RequestManager.__invalidLogin
		elif request["type"].startswith('GET_ITEM'):
			if not "itemId" in request:
				return RequestManager.__invalidRequest
			answer = False
			if request['type'] == 'GET_ITEM_NAME':
				answer = self.__systemManager.getItemName(request["login"], request['itemId'])
			elif request['type'] == 'GET_ITEM_DATA':
				answer = self.__systemManager.getItemData(request["login"], request['itemId'])
			elif request['type'] == 'GET_ITEM_TYPE':
				answer = self.__systemManager.getItemType(request["login"], request['itemId'])
			elif request['type'] == 'GET_ITEM_PARENT':
				answer = self.__systemManager.getItemParentId(request["login"], request['itemId'])
			if type(answer) is bool and not answer:
				return RequestManager.__invalidRequest
			return {"status": "OK", "code": 200, "answer": answer}

		elif request["type"] == "CREATE_FOLDER":
			if not "where" in request:
				return RequestManager.__invalidRequest
			if not "name" in request:
				return RequestManager.__invalidRequest
			createdId = self.__systemManager.createFolder(request['login'], request['name'], request['where'])
			if type(createdId) is bool and not createdId:
				return RequestManager.__invalidRequest
			return {"status": "OK", "code": 200, "answer": createdId}
		elif request["type"] == "CREATE_FILE":
			if not "where" in request:
				return RequestManager.__invalidRequest
			if not "name" in request:
				return RequestManager.__invalidRequest
			if not "data" in request:
				return RequestManager.__invalidRequest
			createdId = self.__systemManager.createFile(request['login'], request['name'], request['data'], request['where'])
			if type(createdId) is bool and not createdId:
				return RequestManager.__invalidRequest
			return {"status": "OK", "code": 200, "answer": createdId}
		elif request["type"] == "GET_ROOT_FOLDER":
			client = self.__systemManager.getClient(request['login'])
			return {"status": "OK", "code": 200, "answer": client.getRootFolder()}
		elif request['type'] == 'GET_SHARED_FOLDER':
			client = self.__systemManager.getClient(request['login'])
			return {"status": "OK", "code": 200, "answer": client.getSharedFolder()}
		elif request["type"] == "SHARE_ITEM":
			if not 'itemId' in request or not 'toLogin' in request:
				return RequestManager.__invalidRequest
			if not self.__systemManager.addPermission(request['itemId'], request['login'], request['toLogin']):
				return RequestManager.__invalidRequest
			else:
				return RequestManager.__permissionGiven
		elif request["type"] == "RENAME_ITEM":
			if not 'itemId' in request or not 'newName' in request:
				return RequestManager.__invalidRequest
			if not self.__systemManager.renameItem(request['login'], request['itemId'], request['newName']):
				return RequestManager.__invalidRequest
			else:
				return RequestManager.__itemRenamed
		elif request["type"] == "EDIT_FILE_DATA":
			if not 'fileId' in request or not 'newData' in request:
				return RequestManager.__invalidRequest
			if not self.__systemManager.editFileData(request['login'], request['fileId'], request['newData']):
				return RequestManager.__invalidRequest
			else:
				return RequestManager.__fileEdited
		elif request["type"] == "MOVE_ITEM":
			if not 'itemId' in request or not 'newParent' in request:
				return RequestManager.__invalidRequest
			if not self.__systemManager.moveItem(request['login'], request['itemId'], request['newParent']):
				return RequestManager.__invalidRequest
			else:
				return RequestManager.__itemMoved
		else:
			return RequestManager.__invalidRequest

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

if __name__ == "__main__":
	rm = RequestManager()
	while True:
		req = getReq()
		res = rm.processRequest(req)
		print(str(res))
