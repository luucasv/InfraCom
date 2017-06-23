from DataBase import DataBase

class DataManager:
	def __init__(self, folderDbName = "DataManagerDb"):
		self.__db = DataBase(folderDbName)
		if not self.__db.isValidKey("NextId"):
			self.__db.set("NextId", 0)

	def __createId(self):
		fileId = self.__db.get('NextId')
		self.__db.set('NextId', fileId + 1)
		return str(fileId)

	def newData(self, data):
		dataId = self.__createId()
		self.__db.set(dataId, data)
		return dataId

	def updateData(self, dataId, data):
		if not self.__db.isValidKey(dataId):
			return False
		self.__db.set(dataId, data)
		return True

	def getData(self, dataId):
		if not self.__db.isValidKey(dataId):
			return False
		return self.__db.get(dataId)
