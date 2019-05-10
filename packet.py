

def create_udp_packet(seq, data):

	packet = bytearray()

	# unsigned 2 bytes for Checksum
	packet.extend(calculate_checksum())
	# unsigned 2 bytes for length
	packet.extend((len(data)).to_bytes(2, byteorder='big'))
	# unsigned 4 bytes for sequence number
	packet.extend(seq.to_bytes(4, byteorder='big'))
	# 504 bytes for data
	if isinstance(data, str):
		data = data.encode("utf-8")

	packet.extend(data)

	return packet



def create_udp_ack(seq):

	packet = bytearray()

	# unsigned 2 bytes for Checksum
	packet.extend(calculate_checksum())
	# unsigned 2 bytes for length
	packet.extend((8).to_bytes(2, byteorder='big'))
	# unsigned 4 bytes for sequence number
	packet.extend(seq.to_bytes(4, byteorder='big'))

	return packet	



def calculate_checksum():

	cksum = bytearray()
	cksum.extend((6).to_bytes(2, byteorder='big'))

	return cksum



def packet_parser(packet):

	cksum = packet[0: 2]
	length = int.from_bytes(packet[2: 4], byteorder='big')
	seq_no = int.from_bytes(packet[4: 8], byteorder='big')

	if len(packet) > 8:

		data = packet[8:]

	else:
		data = ""

	return seq_no, data

