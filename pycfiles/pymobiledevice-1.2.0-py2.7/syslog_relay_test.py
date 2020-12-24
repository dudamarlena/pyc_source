# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/syslog_relay_test.py
# Compiled at: 2019-03-03 19:03:36
"""syslog_relay test case
"""
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