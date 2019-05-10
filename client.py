import socket
import packet


def request_file(file_name, server_port, server_ip="127.0.0.1"):

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	client_socket.bind(("", 0))

	request = packet.create_udp_packet(0, file_name)

	client_socket.sendto(request, (server_ip, server_port))





request_file("test", 55055)