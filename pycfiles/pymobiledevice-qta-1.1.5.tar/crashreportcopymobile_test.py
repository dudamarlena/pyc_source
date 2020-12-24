# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/crashreportcopymobile_test.py
# Compiled at: 2019-03-03 18:58:25
__doc__ = 'screenshotr test case\n'
import unittest, os
from pymobiledevice.usbmux.usbmux import USBMux
from pymobiledevice.lockdown import LockdownClient
from pymobiledevice.afc import AFCShell
from pymobiledevice.afc import AFCClient

class CrashReportTest(unittest.TestCase):

    def test_get_crash_log(self):
        mux = USBMux()
        if not mux.devices:
            mux.process(0.1)
        if len(mux.devices) == 0:
            print 'no real device found'
            self.no_device = True
            return
        udid = mux.devices[0].serial
        procname = 'QQ'
        lockdown = LockdownClient(udid)
        self.service = lockdown.startService('com.apple.crashreportcopymobile')
        client = AFCClient(lockdown, service=self.service)
        afc_shell = AFCShell(client=client)
        remote_crash_path = '/'
        dest_path = '/tmp'
        local_crashes = []
        print ('udid:', udid)
        for _dirname, _dirs, files in afc_shell.afc.dir_walk(remote_crash_path):
            for filename in files:
                if procname in filename:
                    remote_crash_file = os.path.join(remote_crash_path, filename)
                    data = afc_shell.afc.get_file_contents(remote_crash_file)
                    local_crash_file = os.path.join(dest_path, filename)
                    local_crashes.append(local_crash_file)
                    with open(local_crash_file, 'wb') as (fp):
                        fp.write(data)

        print local_crashes

    def tearDown(self):
        if not self.no_device and self.service:
            self.service.close()