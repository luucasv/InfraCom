import socket
import sys

def http():
	sock = socket.socket()
	svAddr = ('', 80)
	sock.bind(svAddr)
	sock.listen(1)
	while True:
		conn, addr = sock.accept()
		try:
			f = conn.recv(1024).decode()
			print(f)
			assert(f.split(' ')[0] == "GET")
			print(f.split(' ')[1])
			qry = 'HTTP/1.0 200 OK\r\n'
			qry += 'Content-Type: text/html\r\n\r\n'
			file = open(f.split(' ')[1], "rb")
			conn.sendall(qry.encode() + file.read())
		except IOError:
			conn.sendall("HTTP/1.0 404 Not Found\r\n\r\n".encode())
		except:
			pass
		finally:
			conn.close()



def udp():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	svAddr = ('', 27015)
	sock.bind(svAddr)
	try:
		while True:
			dados, addr = sock.recvfrom(1024)
			print("Dados recebidos de", addr, ":", dados.decode())
			sock.sendto(dados, addr)
	except:
		pass
	finally:
		sock.close()

def tcp():
	sock = socket.socket()
	svAddr = ('', 27015)
	sock.bind(svAddr)

	sock.listen(1)
	while True:
		conn, addr = sock.accept()
		try:
			print("conectado com", addr)

			dados = True
			msg = ""
			while dados:
				dados = conn.recv(1024)
				conn.sendall(dados)
				msg += dados.decode()
			print("Mensagem recebida do cliente: ", msg)
		except:
			pass
		finally:
			print("Finalizando conexao.")
			conn.close()

def main():
	while True:
		print("")
		print("1. TCP")
		print("2. UDP")
		print("3. HTTP")
		op = int(input("Escolha uma das opcoes acima para o servidor: "))
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