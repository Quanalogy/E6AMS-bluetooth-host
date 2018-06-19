import struct
import hashlib

from Layers.DllLayer import DllLayer
from Layers.AppLayer import AppLayer
from Frames.DllFrame import DllFrame
from Frames.AppFrame import AppFrame

md5 = hashlib.md5()

preamble = 0xAA
version = 0x01
command = 0x01 # Control
profil = 0x01
knap = 0x01
payload = struct.pack(">2B", profil, knap)
payload_len = len(payload)

#  version+cmd+len + length of pay+hash
length = 1 + 1 + 2 + payload_len + 16

packet_no_md5 = struct.pack(">BH2BH", preamble, length, version, command, payload_len) + payload
md5.update(packet_no_md5)
packet = packet_no_md5 + md5.digest()

dll_layer = DllLayer(DllFrame)
app_layer = AppLayer(AppFrame)
dll_layer.bind(None, app_layer)
app_layer.bind(dll_layer, None)

# step = int(len(packet) / 3)
#
# for i in range(3):
#     first_index = step*i
#     if i == 2:
#         to_send = packet[first_index:]
#
#     else:
#         to_send = packet[first_index:step*(i+1)]
#
#     dll_layer.receive(None, to_send)

packets = ["aa00150100000101c00abf6723ba72ecfd61f734", "0de6cadaaa001401030000b99ee9adf6a2e46857b10028352fe174"]

for pack in packets:
    dll_layer.receive(None, bytes.fromhex(pack))
