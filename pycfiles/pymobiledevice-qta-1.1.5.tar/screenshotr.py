# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/screenshotr.py
# Compiled at: 2019-03-03 17:04:15
import os, plistlib, logging
from pymobiledevice.lockdown import LockdownClient
from six import PY3
from pprint import pprint
from time import gmtime, strftime
from optparse import OptionParser

class screenshotr(object):

    def __init__(self, lockdown=None, serviceName='com.apple.mobile.screenshotr', udid=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.lockdown = lockdown if lockdown else LockdownClient(udid=udid)
        self.service = self.lockdown.startService(serviceName)
        DLMessageVersionExchange = self.service.recvPlist()
        version_major = DLMessageVersionExchange[1]
        self.service.sendPlist(['DLMessageVersionExchange', 'DLVersionsOk', version_major])
        DLMessageDeviceReady = self.service.recvPlist()

    def stop_session(self):
        self.service.close()

    def take_screenshot(self):
        self.service.sendPlist(['DLMessageProcessMessage', {'MessageType': 'ScreenShotRequest'}])
        res = self.service.recvPlist()
        assert len(res) == 2
        assert res[0] == 'DLMessageProcessMessage'
        if res[1].get('MessageType') == 'ScreenShotReply':
            if PY3:
                screen_data = res[1]['ScreenShotData']
            else:
                screen_data = res[1]['ScreenShotData'].data
            return screen_data
        return


if __name__ == '__main__':
    parser = OptionParser(usage='%prog')
    parser.add_option('-u', '--udid', default=False, action='store', dest='device_udid', metavar='DEVICE_UDID', help='Device udid')
    parser.add_option('-p', '--path', dest='outDir', default=False, help='Output Directory (default: . )', type='string')
    options, args = parser.parse_args()
    outPath = '.'
    if options.outDir:
        outPath = options.outDir
    logging.basicConfig(level=logging.INFO)
    lckdn = LockdownClient(options.device_udid)
    screenshotr = screenshotr(lockdown=lckdn)
    data = screenshotr.take_screenshot()
    if data:
        filename = strftime('screenshot-%Y-%m-%d-%H-%M-%S.tif', gmtime())
        outPath = os.path.join(outPath, filename)
        print 'Saving Screenshot at %s' % outPath
        o = open(outPath, 'wb')
        o.write(data)