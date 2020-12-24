# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/listdevice_test.py
# Compiled at: 2019-03-03 19:02:43
"""Device Query test case
"""
import unittest
from pymobiledevice.usbmux.usbmux import USBMux

class ListDeviceTest(unittest.TestCase):

    def test_list_devices(self):
        mux = USBMux()
        if not mux.devices:
            mux.process(0.1)
        self.assertTrue(len(mux.devices) >= 0, 'usbmuxd communication error')