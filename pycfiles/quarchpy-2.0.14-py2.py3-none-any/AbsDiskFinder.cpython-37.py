# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\AbsDiskFinder.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 377 bytes
from abc import abstractmethod, ABCMeta

class AbsDiskFinder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def returnDisk(self):
        pass

    @abstractmethod
    def findDevices(self):
        pass

    @abstractmethod
    def formatList(self, deviceList):
        pass