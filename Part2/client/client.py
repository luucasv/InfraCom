from ApplicationManager import ApplicationManager
from NetworkManager import NetworkManager
import sys

def main():
	if len(sys.argv) != 3:
		print ('Usage : python3 client.py hostname port')
		sys.exit(1)

	host = sys.argv[1]
	port = int(sys.argv[2])
	
	try:
		NetworkManager.connect((host, port))
	except :
		print('Unable to connect. Maybe the server is not up.')
		sys.exit()
	
	print('Welcome to InfraComDrive betha 2.0.0')
	ApplicationManager.createDownloadFolder()
	while True:
		ApplicationManager.printWorkingDir()
		cmd = input().split()
		ApplicationManager.processCmd(cmd)

if __name__ == '__main__':
	main()