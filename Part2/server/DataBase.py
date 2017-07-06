import os
import pickle

class DataBase:
	def __init__(self, folderName):
		self.__folderName = folderName

		if not os.path.exists(folderName):
			os.makedirs(folderName)

	def isValidKey(self, key):
		return os.path.exists(self.__folderName + '/' + key + ".pkl")

	def set(self, key, data):
		fileName = self.__folderName + "/" + key + ".pkl";
		with open(fileName, 'wb') as file:
			pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)

	def get(self, key):
		fileName = self.__folderName + "/" + key + ".pkl";
		with open(fileName, 'rb') as file:
			db = pickle.load(file)
			return db
