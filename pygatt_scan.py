# Implementation inspired from https://github.com/peplin/pygatt

import pygatt
import logging
import time

from Layers.DllLayer import DllLayer
from Layers.AppLayer import AppLayer
from Frames.DllFrame import DllFrame
from Frames.AppFrame import AppFrame

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

hm10_uuid = "0000FFE1-0000-1000-8000-00805F9B34FB"
hm10_address = "D4:36:39:BB:E8:D6"
# The BGAPI backend will attemt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.GATTToolBackend()

dll_layer = DllLayer(DllFrame)
app_layer = AppLayer(AppFrame)
dll_layer.bind(app_layer)

def handle_data(handle: int, value: bytearray):
    """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
    """
    response = dll_layer.receive(value)

    if response is not None:
        print("This is the response: {}".format(response.hex()))
        # device.w

try:
    adapter.start()
    device = adapter.connect(address=hm10_address)
    val = device.discover_characteristics()
    print("discover_characteristics", val)
    device.subscribe(hm10_uuid, callback=handle_data)
    while True:
        time.sleep(0.1)

finally:
    adapter.stop()