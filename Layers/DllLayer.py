# Implementation inspired from https://github.com/peplin/pygatt
import struct
import pygatt
import logging

from Layers.LayerTemplate import LayerTemplate
from Frames.FrameTemplate import FrameTemplate

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

class DllLayer(LayerTemplate):

    def __init__(self, frame_parser: FrameTemplate):
        super().__init__(frame_parser)
        # The BGAPI backend will attemt to auto-discover the serial device name of the
        # attached BGAPI-compatible USB adapter.
        self.SOF = 0xAA
        self.reset_packet_values()

        self.hm10_uuid = "0000FFE1-0000-1000-8000-00805F9B34FB"
        self.hm10_address = "D4:36:39:BB:E8:D6"
        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start()
        self.device = self.adapter.connect(address=self.hm10_address)
        self.device.subscribe(self.hm10_uuid, callback=self.receive)



    def receive(self, handle: int, packet: bytearray):
        """ Method for handle receive of new packet.

        :param packet:  The packet received in form of: |Preamble|Length
        :return:        Nothing
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
                return

            self.reset_packet_values()

        else:
            if packet[0] == self.SOF:
                self.started = True
                self.remaining = struct.unpack(">H", packet[1:3])[0] - packet_len + 3
                self.totalPacket += packet
                print("Start of frame received, {} bytes remaining".format(self.remaining))
            else:
                print("Throwing away packet as the first byte is not {}, packet: {}".format(self.SOF, packet.hex()))

            return None

    def reset_packet_values(self):
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

    def send(self, packet):
        dll_obj = self.frame_parser.from_appframe(packet)
        self.device.char_write(self.hm10_uuid, dll_obj.frame())