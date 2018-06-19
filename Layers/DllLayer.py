# Implementation inspired from https://github.com/peplin/pygatt
import time
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
        self.offloadedPacket = bytearray()
        self.reset_packet_values()
        self.hm10_uuid = "0000FFE1-0000-1000-8000-00805F9B34FB"
        self.hm10_address = "D4:36:39:BB:E8:D6"
        # self.adapter = pygatt.GATTToolBackend()
        # self.adapter.start()
        self.setup_device()

    def setup_device(self):
        # self.device = self.adapter.connect(address=self.hm10_address)
        # self.device.subscribe(self.hm10_uuid, callback=self.receive)
        pass

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
                self.offloadedPacket = packet[packet_len:]
            # Done receiving, unpack the packet
            response = self.handle_packet(self.totalPacket + packet[:packet_len])

            if response != None:
                print("You need to implement response mate")
                return

            self.reset_packet_values()

        else:
            if packet[0] == self.SOF:
                self.remaining = struct.unpack(">H", packet[1:3])[0] - packet_len + 3

                if self.remaining == 0:
                    self.started = False
                    response = self.handle_packet(packet)

                    if response != None:
                        print("You need to implement response mate")
                        return

                    self.reset_packet_values()
                else:
                    self.started = True
                    self.totalPacket += packet

                print("Start of frame received, {} bytes remaining".format(self.remaining))
            else:
                print("Throwing away packet as the first byte is not {}, packet: {}".format(self.SOF, packet.hex()))

            return None

    def reset_packet_values(self):

        if len(self.offloadedPacket) > 0:
            # We've got some extra data to be handled
            self.started = True
            if self.offloadedPacket[0] == self.SOF:
                # The next packet is there
                self.totalPacket = self.offloadedPacket
            elif self.SOF in self.offloadedPacket:
                self.totalPacket = self.offloadedPacket[self.offloadedPacket.index(self.SOF):]
            else:
                self.totalPacket = bytearray()

            if len(self.totalPacket) > 3:
                self.remaining = struct.unpack(">H", self.totalPacket[1:3])[0]
                if self.remaining <= len(self.totalPacket[3:]):
                    # We have another frame to send

                    while True:
                        offset = self.remaining+3
                        response = self.handle_packet(self.totalPacket[:offset])

                        if response != None:
                            print("You need to implement response mate")
                            return

                        self.totalPacket = self.totalPacket[offset:]

                        if len(self.totalPacket) < 3:
                            break
                        else:
                            self.remaining = struct.unpack(">H", self.totalPacket[1:3])[0]

            else:
                self.remaining = 0
                self.started = False

            self.offloadedPacket = bytearray()
        else:
            self.started = False
            self.remaining = 0
            self.totalPacket = bytearray()
            self.offloadedPacket = bytearray()

    def handle_packet(self, packet):
        dll_frame = self.frame_parser.from_bytes(packet)

        if None != dll_frame:
            app_frame = dll_frame.getPayload()
            if app_frame is not None:
                return self.upper_layer.receive(app_frame)
            else:
                print("App frame is none!")
        else:
            print("DLL frame None")
            print(packet.hex())
            return None

    def send(self, packet):

        if not self.device.bond():
            self.setup_device()

        dll_obj = self.frame_parser.from_appframe(packet)
        print("Got the following DLL frame to send:", dll_obj.frame().hex())

        offset = 20
        frame = dll_obj.frame()
        packet_len = len(frame)
        for i in range(0, packet_len -1, offset):
            if i + offset > packet_len:
                print("send {} bytes".format(packet_len-i))
                self.device.char_write(self.hm10_uuid, frame[i:])
            else:
                print("Send 20 bytes")
                self.device.char_write(self.hm10_uuid, frame[i:i+offset])
            time.sleep(0.01)
