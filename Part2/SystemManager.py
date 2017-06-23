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

	def __canOpen(self, who, itemId):
		if not self.__userExists(who) or not self.__itemExists(itemId):
			return False
		if not self.__fileSystem.canOpen(itemId, who):
			return False
		return True

	def __canCreate(self, who, parentId):
		if parentId == 'root':
			return self.__userExists(who)
		if not self.__canOpen(who, parentId):
			return False
		if self.getClient(who).getSharedFolder() == parentId:
			return False
		return True

	def __isDefaultFolder(self, who, itemId):
		client = self.getClient(who)
		return client.getSharedFolder() == itemId or client.getRootFolder() == itemId

	def getItemName(self, who, itemId):
		if not self.__canOpen(who, itemId):
			return False
		return self.__fileSystem.getItemName(itemId)

	def getItemParentId(self, who, itemId):
		if not self.__canOpen(who, itemId):
			return False
		return self.__fileSystem.getItemParentId(itemId)
	def getItemType(self, who, itemId):
		if not self.__canOpen(who, itemId):
			return False
		return self.__fileSystem.getItemType(itemId)

	def getItemData(self, who, itemId):
		if not self.__canOpen(who, itemId):
			return False
		return self.__fileSystem.getItemData(itemId)

	def getClient(self, login):
		return self.__clientManager.getClient(login)
		
	def createClient(self, login, password):
		if self.__userExists(login):
			return False
		idShared = self.__fileSystem.createFolder(login + "-shared")
		idRoot = self.__fileSystem.createFolder(login + "-root")
		self.__clientManager.createClient(login, password, idRoot, idShared)
		self.__fileSystem.addPermission(idShared, login)
		self.__fileSystem.addPermission(idRoot, login)
		return True

	def createFolder(self, who, folderName, parentId):
		if not self.__canCreate(who, parentId):
			return False
		return self.__fileSystem.createFolder(folderName, parentId)

	def createFile(self, who, fileName, fileData, parentId):
		if not self.__canCreate(who, parentId):
			return False
		return self.__fileSystem.createFile(fileName, fileData, parentId)

	def editFileData(self, who, fileId, newData):
		if not self.__canOpen(who, fileId):
			return False
		return self.__fileSystem.editFileData(fileId, newData)

	def renameItem(self, who, itemId, newName):
		if not self.__canOpen(who, itemId):
			return False
		return self.__fileSystem.renameItem(itemId, newName)

	def moveItem(self, who, itemId, toFolder):
		if not self.__canOpen(who, itemId) or not self.__canOpen(who, toFolder):
			return False
		if self.__isDefaultFolder(who, itemId):
			return False
		return self.__fileSystem.moveItem(itemId, toFolder)

	def addPermission(self, itemId, who, to):
		if not self.__canCreate(who, itemId):
			return False
		if self.__isDefaultFolder(who, itemId):
			return False
		if not self.__userExists(to):
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

