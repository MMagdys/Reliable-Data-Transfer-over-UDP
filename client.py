import socket
import packet


def request_file(file_name, server_port, server_ip="127.0.0.1"):

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	client_socket.settimeout(0.5)
	client_socket.bind(("", 0))

	request = packet.create_udp_packet(0, file_name)

	while 1:

		try:
			client_socket.sendto(request, (server_ip, server_port))
			data_packet, addr = client_socket.recvfrom(1024)
			break

		except socket.timeout:
			continue	

	while 1:

		data_packet, addr = client_socket.recvfrom(1024)
		seq_no, data = packet.packet_parser(data_packet)
		print(data)

		if data == b'EOF':
			ack = packet.create_udp_ack(seq_no)
			break

		with open(file_name, "ab") as f:
			f.write(data)

		ack = packet.create_udp_ack(seq_no)
		client_socket.sendto(ack, addr)
		print(ack)


	client_socket.close()

		


request_file("file1", 55055)