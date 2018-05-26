import struct

from Frames.FrameTemplate import FrameTemplate

class AppFrame(FrameTemplate):

    def __init__(self, command, expected_length, payload):
        self.command = command
        self.expected_length = expected_length
        self.payload = payload

    def __repr__(self):
        return "\n".join(["Command: {}".format(self.command),
                          "Length: {}".format(self.expected_length),
                          "Payload: {}".format(self.payload)])

    def getPayload(self):
        return self.payload

    @classmethod
    def from_bytes(cls, frame):
        command = frame[0]
        expected_length = struct.unpack(">H", frame[1:3])[0]
        real_length = len(frame[3:])

        if real_length != expected_length:
            print("Length of payload is wrong!")
            print("Expected: {}, Real: {}".format(expected_length, real_length))
            return None

        payload = frame[3:]
        return cls.__init__(command, expected_length, payload)