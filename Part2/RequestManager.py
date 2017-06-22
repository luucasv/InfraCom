from SystemManager import SystemManager
import pickle

class RequestManager:
	__invalidRequest = {"status": "Invalid request", "code": 404}
	__loginExists = {"status": "Login already exists", "code": 401}
	__userCreated = {"status": "Register OK", "code": 201, "answer": "user created"}
	__invalidLogin = {"status": "Invalid login or password", "code": 400}
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
		elif request["type"] == "GET":
			if not "itemId" in request:
				return RequestManager.__invalidRequest
			item = self.__systemManager.getItem(request["itemId"], request['login'])
			if type(item) is bool and not item:
				return RequestManager.__invalidRequest
			return {"status": "OK", "code": 200, "answer": pickle.dumps(item, pickle.HIGHEST_PROTOCOL)}
		elif request["type"] == "CREATE_FOLDER":
			if not "where" in request:
				return RequestManager.__invalidRequest
			if not "name" in request:
				return RequestManager.__invalidRequest
			createdId = self.__systemManager.createItem(request['login'], 'folder', request['name'], [], request['where'])
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
			createdId = self.__systemManager.createItem(request['login'], 'file', request['name'], request['data'], request['where'])
			if type(createdId) is bool and not createdId:
				return RequestManager.__invalidRequest
			return {"status": "OK", "code": 200, "answer": createdId}

def getReq():
	req = {}
	req['type'] = input()
	req['login'] = input()
	req['password'] = input()
	if req['type'] == 'GET':
		req['itemId'] = input()
	elif req['type'] == 'CREATE_FILE':
		req['where'] = input()
		req['name'] = input()
		req['data'] = input()
	elif req['type'] == 'CREATE_FOLDER':
		req['where'] = input()
		req['name'] = input()
	return req

if __name__ == "__main__":
	rm = RequestManager()
	while True:
		req = getReq()
		res = rm.processRequest(req)
		if req['type'] == 'GET':
			res['answer'] = pickle.loads(res['answer']).getData()
		print(str(res))
