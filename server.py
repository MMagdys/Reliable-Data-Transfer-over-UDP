import socket
import threading
import RDT


def start_server(server_port, window, rand_seed, loss_prob, server_ip="127.0.0.1"):

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((server_ip, server_port))

	requests_pool = []

	while 1:
		try:
			request, addr = server_socket.recvfrom(1024)
			# print(request, addr)
			requests_pool.append(threading.Thread(target=RDT.RequestHandler, args=(request, addr,window, rand_seed, loss_prob,)))
			requests_pool[-1].start()

		except KeyboardInterrupt:
			break

	for req in requests_pool:
		req.join()



def main():

	with open("server.in", "r") as config:

		parameters = config.read().split("\n")

	start_server(int(parameters[0]), int(parameters[1]), int(parameters[2]), float(parameters[3]))



if __name__ == '__main__':
	main()