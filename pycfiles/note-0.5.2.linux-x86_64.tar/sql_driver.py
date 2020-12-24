# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/note/sql_driver.py
# Compiled at: 2014-12-20 09:55:02
from db_api import dbBaseClass

class sqliteDB(dbBaseClass):

    def __init__(self):
        """

        """
        pass

    def addItem(self, itemType, itemContents, itemID=None):
        """

        """
        pass

    def getItem(self, itemID):
        """

        """
        pass

    def searchForItem(self, searchInfo, resultLimit=20, sortBy='relevance'):
        """

        """
        pass

    def deleteItem(self, itemID):
        """

        """
        pass

    def makeBackupFile(self, dstPath, fileName):
        """

        """
        pass