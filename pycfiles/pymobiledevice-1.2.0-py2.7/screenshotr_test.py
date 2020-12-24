# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/screenshotr_test.py
# Compiled at: 2019-03-03 19:03:07
"""screenshotr test case
"""
import unittest, tempfile
from pymobiledevice.usbmux.usbmux import USBMux
from pymobiledevice.lockdown import LockdownClient
from pymobiledevice.screenshotr import screenshotr

class ScreenshotrTest(unittest.TestCase):

    def test_screenshot(self):
        mux = USBMux()
        if not mux.devices:
            mux.process(0.1)
        if len(mux.devices) == 0:
            print 'no real device found'
            return
        udid = mux.devices[0].serial
        lockdownclient = LockdownClient(udid)
        tiff_file = tempfile.NamedTemporaryFile(suffix='.tiff')
        tiff_file_path = tiff_file.name
        screenshot = screenshotr(lockdownclient)
        data = screenshot.take_screenshot()
        with open(tiff_file_path, 'wb') as (fd):
            fd.write(data)
        screenshot.stop_session()
        tiff_file.close()