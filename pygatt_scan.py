# Implementation inspired from https://github.com/peplin/pygatt
import time
import os

from Layers.DllLayer import DllLayer
from Layers.AppLayer import AppLayer

from Frames.DllFrame import DllFrame
from Frames.AppFrame import AppFrame

dll_layer = DllLayer(DllFrame)
app_layer = AppLayer(AppFrame)

dll_layer.bind(None, app_layer)
app_layer.bind(dll_layer, None)

try:
    while True:
        path = input("Write path to file to firmware upload\n")

        if os.path.exists(path):
            app_layer.sendFWReset(path)
        else:
            print("File does not exist")

        time.sleep(0.1)

finally:
    dll_layer.adapter.stop()