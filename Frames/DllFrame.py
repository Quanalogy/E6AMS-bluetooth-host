import hashlib
import struct

from Frames.FrameTemplate import FrameTemplate

supported_version = 1
supported_preamble = 0xAA

preamble_len = 1
len_len = 2
version_len = 1
hash_len = 16

class DllFrame(FrameTemplate):

    def __init__(self, preamble, length, version, payload, hash, real_packet_length):
        self.preamble = preamble
        self.version = version
        self.payload = payload
        self.hash = hash
        self.length = length
        self.real_packet_length = real_packet_length

    def __repr__(self):
        return "\n".join(["Packet:",
                          "Preamble:\t {}".format(self.preamble),
                          "Version:\t {}".format(self.version),
                          "Payload:\t {}".format(self.payload),
                          "Hash:\t {}".format(self.hash),
                          "Expected length: {}".format(self.length),
                          "Real packet length {}".format(self.real_packet_length)
                          ])

    def getPayload(self):
        """ Method for handle receive of new packet.
        :param packet:  The packet received in form of: |Preamble|Length
        :return:        Response of the packet, None if no response is required or if packet is not valid
        """
        if packetValid(self.preamble, self.length, self.version, self.payload, self.hash, self.real_packet_length):
            return self.payload
        else:
            return None

    def frame(self):
        header = struct.pack(">BHB", self.preamble, self.length, self.version)
        return header + self.payload + self.hash

    @classmethod
    def from_appframe(cls, frame):
        dll_len = version_len + len(frame) + 16
        md5 = hashlib.md5()
        md5.update(struct.pack(">BHB", supported_preamble, dll_len, supported_version) + frame)

        return cls(supported_preamble, dll_len, supported_version, frame, md5.digest(), dll_len)

    @classmethod
    def from_bytes(cls, frame):
        preamble = frame[0]
        expected_length = struct.unpack(">H", frame[1:3])[0]
        version = frame[3]
        payload = frame[4:-16]
        hash = frame[-16:]
        real_length = len(frame[3:])

        if packetValid(preamble, expected_length, version, payload, hash, real_length):
            return cls(preamble, expected_length, version, payload, hash, real_length)
        else:
            return None

def packetValid(preamble, expected_length, version, payload, hash, real_length) -> bool:
    md5 = hashlib.md5()
    md5.update(struct.pack(">BHB", preamble, expected_length, version) + payload)

    if preamble != supported_preamble:
        print("The preamble is wrong!")
        return False
    elif expected_length > real_length:
        print("Packet length short I can't understand.\nExpected: {} != {} real".format(expected_length, real_length))
        return False
    elif expected_length < real_length:
        print("Packet length too long, trying to read is hash is OK.")
    elif version != supported_version:
        print("Version is not equal to the supported version!")
        return False
    elif md5.digest() == hash:
        return True
    else:
        print("Hash not right!")
        return False