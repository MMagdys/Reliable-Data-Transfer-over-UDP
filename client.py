import socket
import packet


def request_file(file_name, server_port, server_ip="127.0.0.1"):

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	client_socket.settimeout(1)
	client_socket.bind(("", 0))

	request = packet.create_udp_packet(0, file_name)

	while 1:

		try:
			client_socket.sendto(request, (server_ip, server_port))
			data_packet, addr = client_socket.recvfrom(1024)
			exp_seq, data = packet.packet_parser(data_packet)
			print(data_packet)
			print("move on")
			break

		except socket.timeout:
			continue	

	while 1:

		data_packet, addr = client_socket.recvfrom(1024)
		# print(data_packet)
		seq_no, data = packet.packet_parser(data_packet)
		# print(data)

		if seq_no == exp_seq:

			if data == b'EOF':
				ack = packet.create_udp_ack(seq_no)
				break
			print(data)
			with open(file_name, "ab") as f:
				f.write(data)

			ack = packet.create_udp_ack(seq_no)
			client_socket.sendto(ack, addr)
			print(ack)
			exp_seq += 1

		elif seq_no < exp_seq:
			ack = packet.create_udp_ack(seq_no)
			client_socket.sendto(ack, addr)



	client_socket.close()

		


request_file("file1", 55055)