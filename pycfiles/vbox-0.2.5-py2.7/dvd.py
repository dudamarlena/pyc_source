# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\pyVb\disks\dvd\dvd.py
# Compiled at: 2013-03-20 09:41:35
from .. import base

class Dvd(base.RemovableMedium):
    fname = property(lambda s: s.info['Location'])

    def getVmAttachType(self):
        return 'dvddrive'


class GuestAdditions(Dvd):
    fname = property(lambda s: None)

    def getVmAttachMedium(self):
        return 'additions'


class EmptyDvd(GuestAdditions):

    def getVmAttachMedium(self):
        return 'emptydrive'