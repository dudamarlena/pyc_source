# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/credentials/offlineregistry.py
# Compiled at: 2016-12-29 01:49:52
from impacket import winregistry

class OfflineRegistry:

    def __init__(self, hiveFile=None, isRemote=False):
        self.__hiveFile = hiveFile
        if self.__hiveFile is not None:
            self.__registryHive = winregistry.Registry(self.__hiveFile, isRemote)
        return

    def enumKey(self, searchKey):
        parentKey = self.__registryHive.findKey(searchKey)
        if parentKey is None:
            return
        else:
            keys = self.__registryHive.enumKey(parentKey)
            return keys

    def enumValues(self, searchKey):
        key = self.__registryHive.findKey(searchKey)
        if key is None:
            return
        else:
            values = self.__registryHive.enumValues(key)
            return values

    def getValue(self, keyValue):
        value = self.__registryHive.getValue(keyValue)
        if value is None:
            return
        else:
            return value

    def getClass(self, className):
        value = self.__registryHive.getClass(className)
        if value is None:
            return
        else:
            return value

    def finish(self):
        if self.__hiveFile is not None:
            self.__registryHive.close()
        return