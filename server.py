import socket
import threading
import RDT


def start_server(server_port, window, rand_seed, loss_prob, server_ip="127.0.0.1"):

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((server_ip, server_port))

	while 1:
		request, addr = server_socket.recvfrom(1024)
		print(request, addr)
		threading.Thread(target=RDT.RequestHandler, args=(request, addr,window, rand_seed, loss_prob,)).start()


def main():
	start_server(55055, 2, 0,0)


if __name__ == '__main__':
	main()