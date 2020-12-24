# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/afc_test.py
# Compiled at: 2019-03-03 18:58:04
__doc__ = 'afc test case\n'
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