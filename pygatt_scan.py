# Implementation taken from https://github.com/peplin/pygatt

import pygatt
import logging
from binascii import hexlify

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

def handle_data(handle, value):
    """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
    print("Received data: %s" % hexlify(value))


hm10_uuid = "FFE0"
hm10_address = "D4:36:39:BB:E8:D6"
# The BGAPI backend will attemt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.GATTToolBackend()

try:
    adapter.start()
    device = adapter.connect(address=hm10_address)
    # value = device.char_read(hm10_uuid)
    device.subscribe(hm10_uuid, callback=handle_data)
finally:
    adapter.stop()