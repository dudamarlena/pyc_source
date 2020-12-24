# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/note/db_api.py
# Compiled at: 2014-12-20 09:55:02
from abc import ABCMeta, abstractmethod

class dbBaseClass(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def addItem(self, itemType, itemContents, itemID=None):
        pass

    @abstractmethod
    def getItem(self, itemID):
        pass

    @abstractmethod
    def searchForItem(self, searchInfo, resultLimit=20, sortBy='relevance'):
        pass

    @abstractmethod
    def deleteItem(self, itemID):
        pass

    @abstractmethod
    def makeBackupFile(self, dstPath, fileName):
        pass