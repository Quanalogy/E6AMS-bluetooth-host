from Layers.LayerTemplate import LayerTemplate
from Frames.DllFrame import DllFrame

class DllLayer(LayerTemplate):


    def receive(self, packet):
        """ Method for handle receive of new packet.

        :param packet:  The packet received in form of: |Preamble|Length
        :return:        Response of the packet, None if no response is required.
        """

        dll_frame = self.frame_parser.from_bytes(packet)

        if None != dll_frame:
            app_frame = dll_frame.getPayload()
            if app_frame is not None:
                return self.lower_layer.receive(app_frame)
            else:
                print("App frame is none!")
        else:
            print("DLL frame None")
            print(packet.hex())
            return None


# payload = bytes.fromhex("0001bbcc")
# md5_sum = hashlib.md5(payload).digest()
# dll = DllLayer(payload + md5_sum)
# print(dll.valid)