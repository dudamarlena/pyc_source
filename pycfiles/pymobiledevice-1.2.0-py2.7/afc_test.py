# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/afc_test.py
# Compiled at: 2019-03-03 18:58:04
"""afc test case
"""
import unittest
from pymobiledevice.usbmux.usbmux import USBMux
from pymobiledevice.lockdown import LockdownClient
from pymobiledevice.afc import AFCShell

class AfcTest(unittest.TestCase):

    def _get_device(self):
        retry_times = 5
        udid = None
        mux = USBMux()
        if not mux.devices:
            mux.process(0.1)
        while retry_times > 0:
            if len(mux.devices) > 0:
                udid = mux.devices[0].serial
                break
            mux.process(0.5)
            retry_times -= 1

        return udid

    def test_get_device_info(self):
        udid = self._get_device()
        print 'udid:%s' % udid
        if udid is None:
            print 'no real device found'
            return
        else:
            lockdown = LockdownClient(udid)
            lockdown.startService('com.apple.afc')
            info = lockdown.allValues
            print info
            self.assertIsInstance(info, dict, 'Query device information error')
            return

    def test_exec_cmd(self):
        udid = self._get_device()
        print 'udid:%s' % udid
        if udid is None:
            print 'no real device found'
            return
        else:
            AFCShell().onecmd('Hello iPhone!')
            return