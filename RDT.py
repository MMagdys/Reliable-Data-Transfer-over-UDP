import socket
import random
import packet


class RequestHandler(object):

	def __init__(self, request, addr, window, rand_seed, loss_prob, method="stop_and_wait", server_addr="127.0.0.1"):

		self.dest_addr = addr
		self.window_size = window
		# self.rand_seed = rand_seed
		random.seed(rand_seed)
		self.loss_prob = loss_prob
		self.server_addr = server_addr
		self.max_data_size = 500

		self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.data_socket.bind((self.server_addr, 0))
		# self.data_socket.settimeout(0.5)

		print(request)

		self.seq_no, self.file_name = packet.packet_parser(request)
		self.data_socket.sendto(packet.create_udp_ack(self.seq_no), self.dest_addr)
		self.file_name = self.file_name.decode("utf-8")
		print(self.file_name)

		if method == "stop_and_wait":
			self.stop_wait()

		elif method == "selective_repeat":
			pass



	def stop_wait(self):
		
		self.seq_no = random.randrange(65536)

		with open("tests/" + self.file_name, "rb") as f :

			data = f.read(self.max_data_size)

			while data:
				data_packet = packet.create_udp_packet(self.seq_no, data)
				print(data_packet)
				self.data_socket.sendto(data_packet, self.dest_addr)
				ack = self.data_socket.recvfrom(1024)
				print("ACK:: ") 
				print(ack)
				data = f.read(self.max_data_size)
				self.seq_no = ( self.seq_no + 1 ) % 65538

		data_packet = packet.create_udp_packet(self.seq_no, "EOF")
		self.data_socket.sendto(data_packet, self.dest_addr)
		ack = self.data_socket.recvfrom(1024)

		self.data_socket.close()



		


