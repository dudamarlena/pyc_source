# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wmdlib\lowlevel\devicedict.py
# Compiled at: 2007-09-10 19:02:44
"""
This module manages a single dictionary of Windows Media Device Instances

The only public variable is the 'devices' dictionary.
The dictionary is always held up to date by checking for device events before
accessing.

Basic usage:

import wmdlib.lowlevel.devicedict as wmdevdict

#mydevice is IWMDMDevice instance
mydevice = wmdevdict.devices['devicename as shown in explorer']
"""
from wmdlib.lowlevel.MediaDevMgrFactory import GetWMDeviceManager
from UserDict import DictMixin
from comtypes.client import GetEvents, PumpWaitingMessages
from wmdlib.lowlevel.mswmdm import IWMDMNotification
import threading
__all__ = [
 'devices']
_wmdm = GetWMDeviceManager()
_devices = _wmdm.GetDevices()
_devicesUpdated = threading.Event()
_devicesUpdated.set()

class _EventResponder:
    __module__ = __name__

    def WMDMMessage(self, this, *args, **kwargs):
        try:
            _devicesUpdated.clear()
            _devices.clear()
            _devices.update(_wmdm.GetDevices())
        finally:
            _devicesUpdated.set()
        return 0


_eventresponder = _EventResponder()
_eventgetter = GetEvents(_wmdm, _eventresponder, interface=IWMDMNotification)

class _devicesAccess(DictMixin):
    """Controls access to the _devices dict. Makes sure, the dict is updated if
    devices are plugged in or out"""
    __module__ = __name__

    def __getitem__(self, key):
        PumpWaitingMessages()
        _devicesUpdated.wait()
        return _devices[key]

    def keys(self):
        PumpWaitingMessages()
        _devicesUpdated.wait()
        return _devices.keys()


devices = _devicesAccess()