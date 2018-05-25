import hashlib
import struct

from Layers.LayerTemplate import LayerTemplate

class DllLayer(LayerTemplate):


    def receive(self, packet):
        """ Method for handle receive of new packet.

        :param packet:  The packet received in form of: |Preamble|Length
        :return:        Response of the packet, None if no response is required.
        """

        dll_frame = self.frame_parser.from_bytes(packet)

        if None != dll_frame:
            response = self.lower_layer.receive(dll_frame.getPayload())
        else:
            print("DLL frame None")
            print(packet.hex())
            return None

        preamble = packet[0]
        expected_packet_length = packet[1:3]
        real_packet_length = len(packet[1:])
        version = packet[3]

        if preamble != self.supported_preamble:
            return printAndReturnNone("The preamble is wrong!")
        elif expected_packet_length > real_packet_length:
            return printAndReturnNone("Packet length short I can't understand.")
        elif expected_packet_length < real_packet_length:
            print("Packet length too long, trying to read is hash is OK.")
        elif version != self.supported_version:
            return printAndReturnNone("Version is not equal to the supported version!")

        payload = packet[4:-16]
        hash = packet[-16:]

        if packetValid(preamble, expected_packet_length, version, payload, hash):
            # TODO Implement logic
            pass
        else:
            return None

def printAndReturnNone(to_user):
    print(to_user)
    return None

def packetValid(preamble, length, version, payload, hash) -> bool:
    md5 = hashlib.md5()
    md5.update(struct.pack(">BHB", preamble, length, version) + payload)

    if md5.digest() == hash:
        return True
    else:
        print("Hash not right!")

    return False

"""
>>> payload = bytes.fromhex("00aabbcc")
>>> md5_sum = hashlib.md5(payload).digest()
>>> dll = DllLayer(payload + md5_sum)
>>> print(dll.valid)
"""
payload = bytes.fromhex("0001bbcc")
md5_sum = hashlib.md5(payload).digest()
dll = DllLayer(payload + md5_sum)
print(dll.valid)