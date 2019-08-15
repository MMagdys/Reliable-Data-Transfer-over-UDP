

def create_udp_packet(seq, data):

	packet = bytearray()

	if isinstance(data, str):
		data = data.encode("utf-8")

	# unsigned 2 bytes for Checksum
	packet.extend(calculate_checksum(data))
	# unsigned 2 bytes for length
	packet.extend((len(data)).to_bytes(2, byteorder='big'))
	# unsigned 4 bytes for sequence number
	packet.extend(seq.to_bytes(4, byteorder='big'))
	# 504 bytes for data
	packet.extend(data)

	return packet



def create_udp_ack(seq):

	packet = bytearray()

	# unsigned 2 bytes for Checksum
	packet.extend(calculate_checksum("ACK".encode("utf-8")))
	# unsigned 2 bytes for length
	packet.extend((8).to_bytes(2, byteorder='big'))
	# unsigned 4 bytes for sequence number
	packet.extend(seq.to_bytes(4, byteorder='big'))

	return packet	



def calculate_checksum(data):

	chksum = 0
	data_array = bytearray(data)

	if len(data_array) % 2 == 1:
		data_array.append(ord('\0'))

	for i in range(0, len(data_array), 2):
		data = ((data_array[i] << 8) & 0xFF00) | ((data_array[i+1]) & 0xFF)
		chksum += data

		# Carry
		if chksum & 0xFFFF0000 > 1:
			chksum = chksum & 0xFFFF
			chksum += 1

	# 1's complement
	chksum = ~chksum & 0xFFFF

	cksum = bytearray()
	cksum.extend((chksum).to_bytes(2, byteorder='big'))

	# print(chksum)
	# print(cksum)
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



def validate_checksum(data):

	tmp = bytearray(data)
	total = 0

	if len(tmp) % 2 == 1:
		tmp.append(ord('\0'))

	for i in range(0, len(tmp), 2):
		temp = ((tmp[i] << 8) & 0xFF00) | ((tmp[i+1]) & 0xFF)
		total += temp
		if total & 0xFFFF0000 > 1:
			total = total & 0xFFFF
			total += 1
	
	print(total)
	return total == 0xffff