import os
import enum
import queue
import struct
import time

from Layers.LayerTemplate import LayerTemplate
from Frames.FrameTemplate import FrameTemplate

from Misc.Commands import Commands
from Misc.Buttons import profile_mapping

# class fwStates(enum):
#     awiting = 0
#     reset_to_firmware = 1
#     more_to_send = 2

class AppLayer(LayerTemplate):

    def __init__(self, frame_parser: FrameTemplate):
        super().__init__(frame_parser)
        self.sendingQueue = queue.Queue()
        self.lastElement = None
        # self.path_to_firmware = "/home/munk/CLionProjects/E6AMS-Project/cmake-build-release/E6AMS.bin"
        # self.fwState = fwStates.awiting

    def receive(self, packet):

        app_frame = self.frame_parser.from_bytes(packet)

        if app_frame is None:
            print("App frame is None")
            return None

        command = app_frame.command

        if command == Commands.ack_nack:
            #print("AckNack, ", app_frame.getPayload())
            if struct.unpack(">B", app_frame.getPayload())[0] == 0: # Nack
                print("Resending package: ", self.lastElement.hex())
                self.lower_layer.send(self.lastElement)
                return
            else:
                print("Ack")
        elif command == Commands.control:
            xdo_cmd = "DISPLAY=:0 xdotool search impress click {}"
            payload = app_frame.getPayload()
            profile = payload[0]
            button = payload[1]
            os.system(xdo_cmd.format(profile_mapping[profile][button]))
            print("pressed", profile_mapping[profile][button])
            return
        elif command == Commands.firmware_ready_to_accept:
            self.setupAppFrames()
        else:
            raise NotImplementedError("Did not implement command: {}".format(command))

        if not self.sendingQueue.empty():
            self.lastElement = self.sendingQueue.get()
            print("sending: ", self.lastElement.hex())
            time.sleep(10)
            self.lower_layer.send(self.lastElement)

    def sendFWReset(self, path_to_firmware):
        self.path_to_firmware = path_to_firmware
        app_frame_obj = self.frame_parser(Commands.firmware_reset.value, 0, 0)
        print("Sending the following frame:", app_frame_obj.frame().hex())
        # self.fwState = fwStates.reset_to_firmware
        self.lower_layer.send(app_frame_obj.frame())

    def sendMaxProfiles(self):
        app_frame_obj = self.frame_parser(Commands.max_profiles, 1, len(profile_mapping))

    def setupAppFrames(self):
        to_send = []
        with open(self.path_to_firmware, 'rb') as file:

            for_later = bytearray()
            for binLine in file:

                if len(for_later) > 0:
                    binLine = for_later + binLine
                    for_later = bytearray()

                bin_len = len(binLine)
                print("bin_len: ", bin_len)

                for i in range(0, bin_len, 64):
                    if bin_len - (i + 64) >= 0:
                        to_send.append(self.frame_parser(Commands.firmware_segment, 64, binLine[i:i + 64]).frame())
                    else:
                        for_later += binLine[i:]

            if len(for_later) > 0:
                to_send.append(self.frame_parser(Commands.firmware_segment, len(for_later), for_later).frame())

        total_amount_of_segments = len(to_send)

        self.sendingQueue.put(
            self.frame_parser(Commands.firmware_segment_count, 2, struct.pack(">H", total_amount_of_segments)).frame())

        for segment in to_send:
            self.sendingQueue.put(segment)