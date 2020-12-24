# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/diagnostics_relay_test.py
# Compiled at: 2019-03-03 18:58:42
"""diagnostics_relay test case
"""
import unittest, time
from pymobiledevice.usbmux.usbmux import USBMux
from pymobiledevice.lockdown import LockdownClient
from pymobiledevice.diagnostics_relay import DIAGClient

class DiagnosticsRelayTest(unittest.TestCase):

    def test_reboot_device(self):
        mux = USBMux()
        if not mux.devices:
            mux.process(0.1)
        if len(mux.devices) == 0:
            print 'no real device found'
            return
        udid = mux.devices[0].serial
        lockdown = LockdownClient(udid)
        DIAGClient(lockdown).restart()
        time.sleep(10)
        for _ in range(20):
            mux.process(1)
            for dev in mux.devices:
                if udid == dev.serial:
                    print 'reboot successfully'
                    return

        else:
            self.fail('reboot error: real device disconect')