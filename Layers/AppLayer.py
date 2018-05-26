import os

from Layers.LayerTemplate import LayerTemplate
from Misc.Commands import Commands
from Misc.Buttons import profile_mapping

class AppLayer(LayerTemplate):

    def receive(self, packet):

        app_frame = self.frame_parser.from_bytes(packet)

        if app_frame is None:
            print("App frame is None")
            return None

        command = app_frame.command

        if command == Commands.ack_nack:
            pass
        elif command == Commands.control:
            xdo_cmd = "xdotool search impress click {}"
            payload = app_frame.getPayload()
            profile = payload[0]
            button = payload[1]
            os.system(xdo_cmd.format(profile_mapping[profile][button]))
            print("pressed", profile_mapping[profile][button])
        elif command == Commands.firmware_ready_to_accept:
            pass
        elif command == Commands.firmware_reset:
            pass
        elif command == Commands.firmware_segment:
            pass
        elif command == Commands.firmware_segment_count:
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
