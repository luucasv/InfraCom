from SystemManager import SystemManager

class RequestManager:
	def __init__(self):
		self.__systemManager = SystemManager()

	def processRequest(self, request):
		if not "type" in request:
			self.__sendResponse({"status": "Invalid request", "code": 404});
		elif not "login" in request or not "password" in request:
			self.__sendResponse({"status": "Invalid request", "code": 404});

		elif request["type"] == "GET":
			if not "itemId" in request:
				return False
