from ClientManager import ClientManager
from FileSystem import FileSystem

class SystemManager:
	def __init__(self):
		self.__fileSystem = FileSystem()
		self.__clientManager = ClientManager()

	def __userExists(self, login):
		return self.__clientManager.isValidLogin(login)

	def __itemExists(self, itemId):
		return self.__fileSystem.itemExists(itemId)

	def getItem(self, itemId, who):
		if not self.__userExists(who) or not self.__itemExists(itemId):
			return False
		if not self.__fileSystem.canOpen(itemId, who):
			return False
		return self.__fileSystem.getItem(itemId)

	def getClient(self, login):
		return self.__clientManager.getClient(login)
		
	def createClient(self, login, password):
		if self.__userExists(login):
			return False
		idShared = self.__fileSystem.createFolder(login + "-shared")
		idRoot = self.__fileSystem.createFolder(login + "-root")
		self.__clientManager.crateClient(login, password, idRoot, idShared)
		self.__fileSystem.addPermission(idShared, login)
		self.__fileSystem.addPermission(idRoot, login)
		return True

	def createItem(self, who, type, itemName, itemData, parentId = "root"):
		if not self.__userExists(who):
			return False
		client = self.getClient(who)
		if parentId == 'root':
			parentId = client.getRootFolder()
		if client.getSharedFolder() == parentId:
			return False
		if not self.__itemExists(parentId):
			return False
		if not self.__fileSystem.canOpen(parentId, who):
			return False
		return self.__fileSystem.createItem(itemName, itemData, type, parentId)

	def addPermision(self, itemId, who, to):
		if not self.__userExists(who) or not self.__userExists(to):
			return False

		if not self.__fileSystem.canOpen(itemId, who):
			return False

		whoClient = self.getClient(who)
		if whoClient.getSharedFolder() == itemId:
			return False

		if self.__fileSystem.canOpen(itemId, to):
			return True

		toClient = self.getClient(to)
		self.__fileSystem.addPermission(itemId, to)
		self.__fileSystem.insertIdIntoFolderList(toClient.getSharedFolder(), itemId)
		return True

	def authenticate(self, login, password):
		if not self.__userExists(login):
			return False
		return self.__clientManager.authenticate(login, password)

