from DataBase import DataBase

class Client:
	def __init__(self, login, password, rootFolder, sharedFolder):
		self.__rootFolder = rootFolder
		self.__sharedFolder = sharedFolder
		self.__login = login
		self.__password = password

	def getLogin(self):
		return self.__login

	def getRootFolder(self):
		return self.__rootFolder

	def getSharedFolder(self):
		return self.__sharedFolder

	def checkPassword(self, password):
		return (self.__password == password)

class ClientManager:
	def __init__(self, folderDbName = "ClientManagerDb"):
		self.__db = DataBase(folderDbName)

	def createClient(self, login, password, rootFolder, sharedFolder):
		client = Client(login, password, rootFolder, sharedFolder)
		self.__db.set(login, client)

	def getClient(self, login):
		return self.__db.get(login)

	def isValidLogin(self, login):
		return self.__db.isValidKey(login)

	def authenticate(self, login, password):
		return self.getClient(login).checkPassword(password);
