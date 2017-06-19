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
		self.__usersAllowed = {}

	def isFolder(self):
		return self.__type == 'folder'

	def addItem(self, itemId):
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

	def addPermission(self, userId):
		self.__usersAllowed = self.__usersAllowed | {userId}

	def canOpen(self, userId):
		return userId in self.__usersAllowed

class FileSystem:
	def __createId(self):
		fileId = self.__db.get('NextId')
		self.__db.add('NextId', fileId + 1)
		return str(fileId)

	def __init__(self, folderDbName = "FileSystemDb"):
		self.__db = DataBase(folderDbName)
		self.__baseFolder = "0"
		# se não tem o item que guarda o próximo item a ser salvo, é pq o banco de dados está vazio
		# então precisamos criar este item e o item da pasta raiz
		if not self.__db.isValidKey("NextId"):
			self.__db.add("NextId", 1);
			baseFolderItem = FileSystemItem("folder","root", self.__baseFolder, self.__baseFolder)
			self.__db.add(self.__baseFolder, baseFolderItem)

	def __saveItem(self, item):
		self.__db.add(item.getId(), item)

	def getItem(self, itemId):
		return self.__db.get(itemId)

	def __createItem(self, itemName, itemData, itemType, parentFolderId):
		if not self.__db.isValidKey(parentFolderId):
			return False;
		
		parentItem = self.getItem(parentFolderId)

		if not parentItem.isFolder():
			return False;

		item = FileSystemItem(itemType, itemName, self.__createId(), parentFolderId, itemData)
		parentItem.addItem(item.getId())
		
		self.__saveItem(parentItem)
		self.__saveItem(item)

		return item.getId()

	def createFolder(self, folderName, parentFolderId = "0"):
		return self.__createItem(folderName, [], 'folder', parentFolderId)

	def createFile(self, fileName, fileData, parentFolderId = "0"):
		return self.__createItem(fileName, fileData, 'file', parentFolderId)

	def addPermission(self, itemId, userId):
		item = self.getItem(itemId)
		item.addPermission(userId)
		self.__saveItem(item)

	def canOpen(self, itemId, userId):
		item = self.getItem(itemId)
		if item.canOpen(userId):
			return True
		else:
			return self.canOpen(item.getParentId(), userId)

def fileSysTest():
	testFs = FileSystem()
	id = testFs.createFolder("Lucas folder")
	testFs.createFile("arq1", "meus dados 1", id)
	testFs.createFile("arq2", "meus dados 2", id)
	folder = testFs.getItem(id)
	print("arquivos da pasta " + folder.getName())
	for it in folder.getData():
		print(testFs.getItem(it).getName())
		print(testFs.getItem(it).getData())

if __name__ == '__main__':
	fileSysTest()