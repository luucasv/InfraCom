class dataBase:
	def __init__(self, fileName):
		self.__fileName = fileName

		if not os.path.exists(fileName):
			with open(fileName, 'w') as file:
				file.write('{}')

	def validKey(self, key):
		with open(self.__fileName, 'r') as file:
			db = json.load(file)
			return key in db

	def add(self, key, data):
		with open(self.__fileName, 'r') as file:
			db = json.load(file)
		db[key] = data
		with open(self.__fileName, 'w') as file:
			json.dump(db, file)

	def get(self, key):
		with open(self.__fileName, 'r') as file:
			db = json.load(file)
			return db[key]
