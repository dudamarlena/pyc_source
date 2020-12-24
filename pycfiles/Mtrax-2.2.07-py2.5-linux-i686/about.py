# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/about.py
# Compiled at: 2008-02-05 17:02:06
import wx

class AboutDialogInfo:

    def __init__(self):
        self.name = self.description = self.version = self.copyright = ''

    def SetName(self, name):
        self.name = name

    def SetDescription(self, desc):
        self.description = desc

    def SetVersion(self, version):
        self.version = version

    def SetCopyright(self, cprt):
        self.copyright = cprt


def AboutBox(info):
    wx.MessageBox('%s version %s\n\n%s\n\ncopyright ©%s' % (info.name, info.version, info.description, info.copyright), 'About %s' % info.name, wx.ICON_INFORMATION)