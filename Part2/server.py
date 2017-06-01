import os
import pickle

# class client:
# 	def __init__(self, name, password):

"""
	A ideia é que cada arquivo e pasta tenha um id único
	daí só os arquivos são salvos na memória, tendo nome igual a tal id
"""

class dataBase:
	def __init__(self, folderName):
		self.__folderName = folderName

		if not os.path.exists(folderName):
			os.makedirs(folderName)

	def validKey(self, key):
		return os.path.exists(self.__folderName + '/' + key + ".pkl")

	def add(self, key, data):
		fileName = self.__folderName + "/" + key + ".pkl";
		with open(fileName, 'wb') as file:
			pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)

	def get(self, key):
		fileName = self.__folderName + "/" + key + ".pkl";
		with open(fileName, 'rb') as file:
			db = pickle.load(file)
			return db

class fileSystemItem:
	def __init__(self, type, name, itemId, parId, fileData = "Not a File"):
		self.__type = type
		self.__name = name
		self.__parId = parId
		self.__itemId = itemId
		if type == 'folder':
			self.__data = []
		else:
			self.__data = fileData

	def addItem(self, itemId):
		if self.__type == 'folder':
			self.__data.append(itemId)

	def isFolder(self):
		return self.__type == 'folder'

	def getId(self):
		return self.__itemId

	def getData(self):
		return self.__data

	def getName(self):
		return self.__name

class fileSystem:
	__NextId = 1
	def __createId():
		fileId = fileSystem.__NextId
		fileSystem.__NextId = fileSystem.__NextId + 1
		return str(fileId)

	def __init__(self, folderDbName = "fileSystemDb"):
		self.__db = dataBase(folderDbName)
		self.__baseFolder = "0"
		baseFolderItem = fileSystemItem("folder","root", self.__baseFolder, self.__baseFolder)
		self.__db.add(self.__baseFolder, baseFolderItem)

	def __saveItem(self, item):
		self.__db.add(item.getId(), item)

	def creatFolder(self, folderName, parentFolderId = "0"):
		if not self.__db.validKey(parentFolderId):
			print("Not valid parent folder id!!!");
			return False;

		parentItem = self.__db.get(parentFolderId)

		if not parentItem.isFolder():
			print("Not valid parent folder id!!!");
			return False;

		folderItem = fileSystemItem('folder', folderName, fileSystem.__createId(), parentFolderId)		
		parentItem.addItem(folderItem.getId())
		
		self.__saveItem(parentItem)
		self.__saveItem(folderItem)

		return folderItem.getId()

	def creatFile(self, fileName, fileData, parentFolderId = "0"):
		if not self.__db.validKey(parentFolderId):
			print("Not valid parent folder id!!!")
			return False;

		parentItem = self.__db.get(parentFolderId)


		if not parentItem.isFolder():
			print("Not valid parent folder id!!!")
			return False;

		fileItem = fileSystemItem('file', fileName, fileSystem.__createId(), parentFolderId, fileData)		
		parentItem.addItem(fileItem.getId())
		
		self.__saveItem(parentItem)
		self.__saveItem(fileItem)

		return fileItem.getId()

	def getItem(self, itemId):
		return self.__db.get(itemId)

mainFS = fileSystem();
fdid = mainFS.creatFolder("primeiro folder")
flid = mainFS.creatFile("oi", "um arquivo qualquer!!!", fdid)
print(mainFS.getItem('2').getData())