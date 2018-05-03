# Following code taken from: https://github.com/karulis/pybluez

import time
import os
# bluetooth low energy scan
from bluetooth.ble import DiscoveryService
#from xdo import Xdo

#xdo_obj = Xdo()

#win_id = xdo_obj.select_window_with_click()

#print(win_id)

pointer_name = "bill_gates"
spacer = "======================================"
half_spacer = "--------------------------------------"

service = DiscoveryService("hci0")
devices = service.discover(2)
valid_devices = []
pointer_devices = []

print(spacer)
print("Devices:")
print(half_spacer)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))
    stripped_name = name.strip()
    if  stripped_name != '':
        if stripped_name == pointer_name:
            pointer_devices.append((address.strip(), stripped_name))
        else:
            valid_devices.append((address.strip(), stripped_name))

print(half_spacer)
print()

print(spacer)
print("Valid devices:")
print(half_spacer)


for address, name in valid_devices:
    print("name: {}, address: {}".format(name, address))
    print(half_spacer)

print()
print(spacer)
print("Pointer devices:")
print(half_spacer)

for address, name in pointer_devices:
    print("name: {}, address: {}".format(name, address))
    print(half_spacer)

#impress_str = b'impress'

#$ xdotool search impress click 4
#Defaulting to search window name, class, and classname

#impress_wins = xdo_obj.search_windows(winname=impress_str, winclass=impress_str, winclassname=impress_str)

#win_id = impress_wins[0]

reverse = False

xdo_cmd = "xdotool search impress click {}"
for i in range(10):

    if i % 3 == 0:
        reverse = not reverse

    time.sleep(1)
    if not reverse:
        os.system(xdo_cmd.format(4))
    else:
        os.system(xdo_cmd.format(5))

print()
