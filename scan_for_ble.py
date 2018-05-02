# Following code taken from: https://github.com/karulis/pybluez

import time
# bluetooth low energy scan
from bluetooth.ble import DiscoveryService
from xdo import Xdo

xdo_obj = Xdo()

win_id = xdo_obj.select_window_with_click()

pointer_name = "kim_larsen"
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


reverse = False
for i in range(10):

    if i % 3 == 0:
        reverse = not reverse

    # xdo_obj.click_window(win_id, 5)
    time.sleep(1)
    if not reverse:
        xdo_obj.click_window(win_id, 4)
        # xdo_obj.send_keysequence_window(win_id, "Down", 0.0)
    else:
        xdo_obj.click_window(win_id, 5)
        # xdo_obj.send_keysequence_window(win_id, "Up")

print()