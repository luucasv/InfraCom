import socket
import sys

def http():
	sock = socket.socket()
	serverHost = input('Digite o ip do servidor: ')
	svAddr = (serverHost, 80)
	sock.connect(svAddr)
	try:
		req = 'GET /home.html HTTP/1.0\r\n\r\n'
		sock.sendall(req.encode())
		file = ""
		dados = True
		while dados:
			dados = sock.recv(1024).decode()
			file += dados
		if(file.split(' ')[1] == "200"):
			print(file.split("\r\n\r\n")[1])
		else:
			print(file)

	finally:
		sock.close()
	


def udp():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverHost = input('Digite o ip do servidor: ')
	svAddr = (serverHost, 27015)
	myaddr = ('', 27018)
	sock.bind(myaddr)
	dados = str(input("Digite uma mensagem a ser enviada: "))
	tot = len(dados)
	if tot > 1024:
		print("mensagem muito grande para um datagrama UDP")
		return
	sock.sendto(dados.encode(), svAddr)
	while True:
		dados, addr = sock.recvfrom(1024)
		if not dados:
			break
		print("Resposta do servidor: ", dados.decode())
		tot -= len(dados)
		if tot <= 0:
			break

def tcp():
	sock = socket.socket()
	serverHost = input('Digite o ip do servidor: ')
	svAddr = (serverHost, 27015)
	sock.connect(svAddr)

	try:
		dados = str(input("Digite uma mensagem a ser enviada: "))
		sock.sendall(dados.encode())
		tot = len(dados)
		msg = ""
		while tot > 0:
			dados = sock.recv(1024)
			tot -= len(dados)
			msg += dados.decode()
		print("Resposta do servidor:", msg)
	finally:
		sock.close()



def main():
	while True:
		print("")
		print("1. TCP")
		print("2. UDP")
		print("3. HTTP")
		op = int(input("Escolha uma das opcoes acima para enviar dados pro servidor: "))
		if op == 1:
			tcp()
			break
		elif op == 2:
			udp()
			break
		elif op == 3:
			http()
			break
if __name__ == '__main__':
	main()