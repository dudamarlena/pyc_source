# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/syslog_relay_test.py
# Compiled at: 2019-03-03 19:03:36
__doc__ = 'syslog_relay test case\n'
import unittest
from pymobiledevice.usbmux.usbmux import USBMux
from pymobiledevice.syslog import Syslog

class ListDeviceTest(unittest.TestCase):

    def test_list_devices(self):
        mux = USBMux()
        if not mux.devices:
            mux.process(0.1)
        if len(mux.devices) == 0:
            print 'no real device found'
            return
        syslog = Syslog()
        syslog.watch(10, '/tmp/sys.log', 'QQ')