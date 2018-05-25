import os
import time
import struct

from enum import IntEnum

class Commands(IntEnum):
    ack_nack = 0
    control = 1
    firmware_reset = 2
    firmware_ready_to_accept = 3
    firmware_segment_count = 4
    firmware_segment = 5



class AppLayer(object):

    def __init__(self, packet):
        self.command = packet[0]
        self.payload_length = struct.unpack(">H", packet[1:3])[0]
        # Expect        CMD + Len + Payload           + CRC
        expected_length = 1 + 2 + self.payload_length + 4
        real_length = len(packet)

        if real_length > expected_length:
            self.payload = packet[3:self.payload_length]
            print("Something is wrong here, expected length of {} is less than real length of {}".format(expected_length, real_length))
            print("The payload were: {}".format(self.payload.hex()))
        if real_length < expected_length:
            self.payload = packet[3:]
            print("Something is wrong here, expected length of {} is less than real length of {}".format(expected_length, real_length))
            print("The payload were: {}".format(self.payload.hex()))
        else:
            self.payload = packet[3:]

        self.handle_command()

    def handle_command(self):
        # impress_str = b'impress'

        # $ xdotool search impress click 4
        # Defaulting to search window name, class, and classname

        # impress_wins = xdo_obj.search_windows(winname=impress_str, winclass=impress_str, winclassname=impress_str)

        # win_id = impress_wins[0]

        if self.command == Commands.ack_nack:
            pass
        elif self.command == Commands.control:
            xdo_cmd = "xdotool search impress click {}"
            os.system(xdo_cmd.format(4 + (self.payload%2)))
        elif self.command == Commands.firmware_ready_to_accept:
            pass
        elif self.command == Commands.firmware_reset:
            pass
        elif self.command == Commands.firmware_segment:
            pass
        elif self.command == Commands.firmware_segment_count:
            pass
        #
        #
        # reverse = False
        #
        # xdo_cmd = "xdotool search impress click {}"
        # for i in range(10):
        #
        #     if i % 3 == 0:
        #         reverse = not reverse
        #
        #     time.sleep(1)
        #     if not reverse:
        #         os.system(xdo_cmd.format(4))
        #     else:
        #         os.system(xdo_cmd.format(5))
        #
        # print()
