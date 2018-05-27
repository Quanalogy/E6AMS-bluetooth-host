import struct

from Frames.FrameTemplate import FrameTemplate
from Layers.LayerTemplate import LayerTemplate
from Frames.DllFrame import DllFrame

class DllLayer(LayerTemplate):

    SOF = 0xAA
    started = False
    remaining = 0
    totalPacket = bytearray()

    def receive(self, packet):
        """ Method for handle receive of new packet.

        :param packet:  The packet received in form of: |Preamble|Length
        :return:        Response of the packet, None if no response is required.
        """

        packet_len = len(packet)

        if self.started:

            if self.remaining > packet_len:
                self.totalPacket += packet
                self.remaining -= packet_len
                print("Frame received, {} bytes remaining".format(self.remaining))
                return None
            elif self.remaining < packet_len:
                print("Got more remaining than expected, trying to handle anyways")
                packet_len = self.remaining
            # Done receiving, unpack the packet
            self.totalPacket += packet[:packet_len]
            response = self.handle_packet()

            if response != None:
                print("You need to implement response mate")
                return response

            self.resetPacketValues()

        else:
            if packet[0] == self.SOF:
                self.started = True
                self.remaining = struct.unpack(">H", packet[1:3])[0] - packet_len + 3
                self.totalPacket += packet
                print("Start of frame received, {} bytes remaining".format(self.remaining))
            else:
                print("Throwing away packet as the first byte is not {}, packet: {}".format(self.SOF, packet.hex()))

            return None


    def resetPacketValues(self):
        self.started = False
        self.remaining = 0
        self.totalPacket = bytearray()


    def handle_packet(self):
        dll_frame = self.frame_parser.from_bytes(self.totalPacket)

        if None != dll_frame:
            app_frame = dll_frame.getPayload()
            if app_frame is not None:
                return self.lower_layer.receive(app_frame)
            else:
                print("App frame is none!")
        else:
            print("DLL frame None")
            print(self.totalPacket.hex())
            return None


# payload = bytes.fromhex("0001bbcc")
# md5_sum = hashlib.md5(payload).digest()
# dll = DllLayer(payload + md5_sum)
# print(dll.valid)