# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wmdlib\tests\test_lowlevel.py
# Compiled at: 2007-09-10 18:56:48
from wmdlib.lowlevel.mswmdm import *
from wmdlib.lowlevel import MediaDevMgrFactory
from comtypes import COMError
import ctypes
from wmdlib.lowlevel.errorcodes import *
from wmdlib.tests.helpers import *
from wmdlib.lowlevel.devicedict import devices
testdevicename = 'COWON D2'

def test_setup():
    devmgr = MediaDevMgrFactory.GetWMDeviceManager()


class TestIWMDMDevice:
    __module__ = __name__

    def setUp(self):
        self.device = devices[testdevicename]

    def test_GetName(self):
        assert self.device.GetName() != '', "Couldn't retrieve name from device"

    def test_GetManufacturer(self):
        assert self.device.GetManufacturer() != '', "Couldn't retrieve manufacturer name from device"

    @com_optional_func
    def test_GetVersion(self):
        version = self.device.GetVersion()

    def test_GetType(self):
        type = self.device.GetType()
        assert type != None
        assert type != 0
        return

    def test_GetStorages(self):
        assert len(self.device.GetStorages()) > 0, "Couldn't get Storages for Device"


class TestIWMDMStorage:
    __module__ = __name__

    def setUp(self):
        self.storage = devices[testdevicename].GetStorages().values()[0]

    def test_GetName(self):
        assert self.storage.GetName() != '', "Couldn't retrieve Name for Storage"

    def test_GetStorages(self):
        assert len(self.storage.GetStorages()) > 0, "Couldn't get Storages for Device"