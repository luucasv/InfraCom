from DataBase import DataBase
from DataManager import DataManager

class FileSystemItem:
	def __init__(self, type, name, itemId, parentId, dataId):
		self.__type = type
		self.__name = name
		self.__parentId = parentId
		self.__itemId = itemId
		self.__dataId = dataId
		self.__usersAllowed = set({})

	def isFolder(self):
		return self.__type == 'folder'

	def getId(self):
		return self.__itemId

	def getDataId(self):
		return self.__dataId

	def getName(self):
		return self.__name

	def getParentId(self):
		return self.__parentId

	def getType(self):
		return self.__type
	
	def canOpen(self, userId):
		return userId in self.__usersAllowed

	def addPermission(self, userId):
		self.__usersAllowed = self.__usersAllowed | {userId}

	def setName(self, newName):
		self.__name = newName

	def setParentId(self, newParent):
		self.__parentId = newParent

class FileSystem:
	def __init__(self, folderDbName = "FileSystemDb"):
		self.__db = DataBase(folderDbName)
		self.__dataManager = DataManager()
		self.__baseFolder = "0"
		# se não tem o item que guarda o próximo item a ser salvo, é pq o banco de dados está vazio
		# então precisamos criar este item e o item da pasta raiz
		if not self.__db.isValidKey("NextId"):
			self.__db.set("NextId", 1)
			baseDataId = self.__dataManager.newData([])
			baseFolderItem = FileSystemItem("folder", "root", self.__baseFolder, self.__baseFolder, baseDataId)
			self.__db.set(self.__baseFolder, baseFolderItem)
	
	def __createId(self):
		fileId = self.__db.get('NextId')
		self.__db.set('NextId', fileId + 1)
		return str(fileId)

	def __saveItem(self, item):
		self.__db.set(item.getId(), item)

	def __getData(self, dataId):
		return self.__dataManager.getData(dataId)

	def __updateData(self, dataId, data):
		self.__dataManager.updateData(dataId, data)

	def __getItem(self, itemId):
		return self.__db.get(itemId)

	def __createItem(self, itemName, itemData, itemType, parentFolderId):
		if not self.itemExists(parentFolderId):
			return False

		parentItem = self.__getItem(parentFolderId)

		if not parentItem.isFolder():
			return False

		dataId = self.__dataManager.newData(itemData)
		item = FileSystemItem(itemType, itemName, self.__createId(), parentFolderId, dataId)
		self.__saveItem(item)
		self.insertIdIntoFolderList(parentFolderId, item.getId())

		return item.getId()

	def itemExists(self, itemId):
		return self.__db.isValidKey(itemId)

	def insertIdIntoFolderList(self, folderId, itemId):
		if not self.itemExists(folderId) or not self.itemExists(itemId):
			return False
		folder = self.__getItem(folderId)
		if not folder.isFolder():
			return False
		dataId = folder.getDataId()
		folderData = self.__getData(dataId)
		folderData.append(itemId)
		self.__updateData(dataId, folderData)
		return True

	def removeIdFromParentList(self, itemId, parentId):
		if not self.itemExists(itemId):
			return False
		parent = self.__getItem(parentId)
		if not parent.isFolder():
			return False
		dataId = parent.getDataId()
		data = self.__getData(dataId)
		data.remove(itemId)
		self.__updateData(dataId, data)
		return True

	def createFolder(self, folderName, parentFolderId = "0"):
		return self.__createItem(folderName, [], 'folder', parentFolderId)

	def createFile(self, fileName, fileData, parentFolderId = "0"):
		return self.__createItem(fileName, fileData, 'file', parentFolderId)

	def editFileData(self, fileId, newData):
		if not self.itemExists(fileId):
			return False
		file = self.__getItem(fileId)
		if file.isFolder():
			return False
		self.__updateData(file.getDataId(), newData)
		return True

	def moveItem(self, itemId, toFolderId):
		if not self.insertIdIntoFolderList(toFolderId, itemId):
			return False
		item = self.__getItem(itemId)
		parentId = item.getParentId()
		if not self.removeIdFromParentList(itemId, parentId):
			return False
		item.setParentId(toFolderId)
		self.__saveItem(item)
		return True

	def renameItem(self, itemId, newName):
		if not self.itemExists(itemId):
			return False
		item = self.__getItem(itemId)
		item.setName(newName)
		self.__saveItem(item)
		return True

	def addPermission(self, itemId, userId):
		item = self.__getItem(itemId)
		item.addPermission(userId)
		self.__saveItem(item)

	def canOpen(self, itemId, userId):
		item = self.__getItem(itemId)
		if itemId == self.__baseFolder:
			return False
		elif item.canOpen(userId):
			return True
		else:
			return self.canOpen(item.getParentId(), userId)

	def getItemName(self, itemId):
		return self.__getItem(itemId).getName()

	def getItemParentId(self, itemId):
		return self.__getItem(itemId).getParentId()

	def getItemType(self, itemId):
		return self.__getItem(itemId).getType()

	def getItemData(self, itemId):
		dataId = self.__getItem(itemId).getDataId()
		return self.__dataManager.getData(dataId)
