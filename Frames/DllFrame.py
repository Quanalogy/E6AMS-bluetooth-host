import hashlib
import struct

from Frames.FrameTemplate import FrameTemplate

class DllFrame(FrameTemplate):

    def __init__(self, preamble, length, version, payload, hash, real_packet_length):
        self.supported_version = 1
        self.supported_preamble = 0xAA
        self.preamble = preamble
        self.version = version
        self.payload = payload
        self.hash = hash
        self.expected_packet_length = length
        self.real_packet_length = real_packet_length

    def __repr__(self):
        return "\n".join(["Packet:",
                          "Preamble:\t {}".format(self.preamble),
                          "Version:\t {}".format(self.version),
                          "Payload:\t {}".format(self.payload),
                          "Hash:\t {}".format(self.hash),
                          "Expected length: {}".format(self.expected_packet_length),
                          "Real packet length {}".format(self.real_packet_length)
                          ])

    def getPayload(self):
        """ Method for handle receive of new packet.
        :param packet:  The packet received in form of: |Preamble|Length
        :return:        Response of the packet, None if no response is required.
        """
        if self.preamble != self.supported_preamble:
            return self.printAndReturnNone("The preamble is wrong!")
        elif self.expected_packet_length > self.real_packet_length:
            return self.printAndReturnNone("Packet length short I can't understand.")
        elif self.expected_packet_length < self.real_packet_length:
            print("Packet length too long, trying to read is hash is OK.")
        elif self.version != self.supported_version:
            return self.printAndReturnNone("Version is not equal to the supported version!")

        if packetValid(self.preamble, self.expected_packet_length, self.version, self.payload, self.hash):
            return self.payload
        else:
            return None

    def from_bytes(cls, frame):
        return cls.__init__(frame[0], frame[1:3], frame[3], frame[4:-16], frame[-16:], len(frame[1:]))

def packetValid(preamble, length, version, payload, hash) -> bool:
    md5 = hashlib.md5()
    md5.update(struct.pack(">BHB", preamble, length, version) + payload)

    if md5.digest() == hash:
        return True
    else:
        print("Hash not right!")

    return False
