

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
	# 504 bytes for data
	packet.extend(data)

	return packet	



def calculate_checksum():
	return bytearray()