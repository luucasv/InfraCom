from DataBase import DataBase

class FileSystemItem:
	def __init__(self, type, name, itemId, parentId, fileData = "Not a File"):
		self.__type = type
		self.__name = name
		self.__parentId = parentId
		self.__itemId = itemId
		if type == 'folder':
			self.__data = []
		else:
			self.__data = fileData
		self.__usersAllowed = set({})

	def isFolder(self):
		return self.__type == 'folder'

	def insertIdIntoFolderList(self, itemId):
		if self.isFolder():
			self.__data.append(itemId)

	def getId(self):
		return self.__itemId

	def getData(self):
		return self.__data

	def getName(self):
		return self.__name

	def getParentId(self):
		return self.__parentId

	def getType(self):
		return self.__type

	def addPermission(self, userId):
		self.__usersAllowed = self.__usersAllowed | {userId}

	def getPermission(self):
		return self.__usersAllowed

	def canOpen(self, userId):
		return userId in self.__usersAllowed

class FileSystem:
	def __init__(self, folderDbName = "FileSystemDb"):
		self.__db = DataBase(folderDbName)
		self.__baseFolder = "0"
		# se não tem o item que guarda o próximo item a ser salvo, é pq o banco de dados está vazio
		# então precisamos criar este item e o item da pasta raiz
		if not self.__db.isValidKey("NextId"):
			self.__db.set("NextId", 1)
			baseFolderItem = FileSystemItem("folder", "root", self.__baseFolder, self.__baseFolder)
			self.__db.set(self.__baseFolder, baseFolderItem)
	
	def __createId(self):
		fileId = self.__db.get('NextId')
		self.__db.set('NextId', fileId + 1)
		return str(fileId)

	def __saveItem(self, item):
		self.__db.set(item.getId(), item)

	def getItem(self, itemId):
		return self.__db.get(itemId)

	def itemExists(self, itemId):
		return self.__db.isValidKey(itemId)

	def createItem(self, itemName, itemData, itemType, parentFolderId):
		if not self.itemExists(parentFolderId):
			return False

		parentItem = self.getItem(parentFolderId)

		if not parentItem.isFolder():
			return False

		item = FileSystemItem(itemType, itemName, self.__createId(), parentFolderId, itemData)
		parentItem.insertIdIntoFolderList(item.getId())

		self.__saveItem(parentItem)
		self.__saveItem(item)

		return item.getId()

	def insertIdIntoFolderList(self, folderId, itemId):
		if not self.itemExists(folderId) or not self.itemExists(itemId):
			return False
		folder = self.getItem(folderId)
		if not folder.isFolder():
			return False
		folder.insertIdIntoFolderList(itemId)
		self.__saveItem(folder)
		return True

	def createFolder(self, folderName, parentFolderId = "0"):
		return self.createItem(folderName, [], 'folder', parentFolderId)

	def createFile(self, fileName, fileData, parentFolderId = "0"):
		return self.createItem(fileName, fileData, 'file', parentFolderId)

	def addPermission(self, itemId, userId):
		item = self.getItem(itemId)
		item.addPermission(userId)
		self.__saveItem(item)

	def canOpen(self, itemId, userId):
		item = self.getItem(itemId)
		if itemId == self.__baseFolder:
			return False
		elif item.canOpen(userId):
			return True
		else:
			return self.canOpen(item.getParentId(), userId)

def fileSysTest():
	testFs = FileSystem()
	id = "0"
	folderItems = list(map(lambda x : testFs.getItem(x).getName(), testFs.getItem(id).getData()))
	print(*folderItems)
	print("Os arquivos da pasta:")
	for i in testFs.getItem(id).getData():
		print(testFs.getItem(i).getName() + ": " + str(list(testFs.getItem(i).getData())))

if __name__ == '__main__':
	fileSysTest()
