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
dll_layer.bind(app_layer)
dll_layer.receive(packet)
