# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/sbservices.py
# Compiled at: 2019-03-03 17:04:38
import logging
from pymobiledevice.lockdown import LockdownClient
from pprint import *
SB_PORTRAIT = 1
SB_PORTRAIT_UPSIDE_DOWN = 2
SB_LANDSCAPE = 3
SB_LANDSCAPE_HOME_TO_LEFT = 4

class SBServiceClient(object):
    service = None

    def __init__(self, lockdown=None, udid=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.lockdown = lockdown if lockdown else LockdownClient(udid=udid)
        if not self.lockdown:
            raise Exception('Unable to start lockdown')
        self.start()

    def start(self):
        self.service = self.lockdown.startService('com.apple.springboardservices')
        if not self.service:
            raise Exception('SBService init error : Could not start com.apple.springboardservices')

    def get_icon_state(self, format_version='2'):
        cmd = {'command': 'getIconState'}
        if format_version:
            cmd['formatVersion'] = format_version
        self.service.sendPlist(cmd)
        res = self.service.recvPlist()
        return res

    def set_icon_state(self, newstate={}):
        cmd = {'command': 'setIconState', 'iconState': newstate}
        self.service.sendPlist(cmd)

    def get_icon_pngdata(self, bid):
        cmd = {'command': 'getIconPNGData', 'bundleId': bid}
        self.service.sendPlist(cmd)
        res = self.service.recvPlist()
        pngdata = res.get('pngData')
        if res:
            return pngdata
        else:
            return

    def get_interface_orientation(self):
        cmd = {'command': 'getInterfaceOrientation'}
        self.service.sendPlist(cmd)
        res = self.service.recvPlist()
        return res.get('interfaceOrientation')

    def get_wallpaper_pngdata(self):
        cmd = {'command': 'getHomeScreenWallpaperPNGData'}
        self.service.sendPlist(cmd)
        res = self.service.recvPlist()
        if res:
            return res.get('pngData')
        else:
            return


if __name__ == '__main__':
    s = SBServiceClient()
    print s.get_icon_pngdata('com.apple.weather')