# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/godirect/backend_usb.py
# Compiled at: 2018-11-09 18:34:59
# Size of source mod 2**32: 872 bytes
import hid, logging
from .backend import GoDirectBackend
from .device_usb import GoDirectDeviceUSB

class GoDirectBackendUSB(GoDirectBackend):
    VID = 2295
    PID = 16

    def __init__(self):
        """ Create a GoDirectBackendUSB object for wrapping the hidapi module.
                """
        self._logger = logging.getLogger('godirect')

    def scan(self):
        """ Find all GoDirect devices
                Returns:
                        GoDirectDevice[]: list of discovered GoDirectDevice objects
                """
        devices = []
        for d in hid.enumerate(self.VID, self.PID):
            device = GoDirectDeviceUSB(self)
            device.id = d['path']
            device.vid = self.VID
            device.pid = self.PID
            device.type = 'USB'
            device.name = d['product_string']
            devices.append(device)

        return devices

    def scan_auto(self, threshold):
        pass

    def connect(self, device):
        pass

    def stop(self):
        pass