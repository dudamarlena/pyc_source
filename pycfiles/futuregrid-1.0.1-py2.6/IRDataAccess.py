# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/repository/server/IRDataAccess.py
# Compiled at: 2012-09-06 11:03:15
"""
Data access and persistent

These classes deal with data persistent and access in the file system,
which could be implemented using file or database.
"""
__author__ = 'Fugang Wang'
from futuregrid.image.repository.server.IRTypes import ImgEntry
from futuregrid.image.repository.server.IRTypes import ImgMeta
from futuregrid.image.repository.server.IRTypes import IRUser
import re

class AbstractImgStore(object):

    def __init__(self):
        if type(self) is AbstractImgStore:
            raise Exception('This is an abstract class')
        else:
            self._items = {}

    def getItemUri(self, imgId):
        pass

    def getItem(self, imgId, userId):
        pass

    def addItem(self, imgEntry):
        pass

    def updateItem(self, imgId, imgEntry):
        pass

    def queryStore(self, imgIds, userId):
        pass

    def persistToStore(self, items):
        pass

    def removeItem(self, userId, imgId):
        pass


class AbstractImgMetaStore(object):

    def __init__(self):
        if type(self) is AbstractImgMetaStore:
            raise Exception('This is an abstract class')
        else:
            self._items = {}

    def getItem(self, imgId):
        pass

    def addItem(self, imgMeta):
        pass

    def updateItem(self, imgId, imgEntry):
        pass

    def getItems(self, criteria):
        pass

    def queryStore(self, imgIds):
        pass

    def persistToStore(self, items):
        pass

    def removeItem(self, userId, imgId):
        pass


class AbstractIRUserStore(object):
    """
    User store existing as a file or db
    """

    def __init__(self):
        if type(self) is AbstractImgMetaStore:
            raise Exception('This is an abstract class')
        else:
            self._items = {}

    def getUser(self, userId):
        pass

    def addUser(self, user):
        pass

    def persistToStore(self, users):
        pass

    def uploadValidator(self, userId, imgSize):
        pass


class ImgStoreFS(AbstractImgStore):

    def __init__(self):
        super(ImgStoreFS, self).__init__()
        self._fsloc = 'IRImgStore'

    def getItemUri(self, imgId):
        return self.getItem(imgId)

    def getItem(self, imgId):
        if imgId not in self._items.keys():
            ret = self.queryStore(imgId)
        else:
            ret = self._items[imgId]
        if ret:
            ret = ret._imgURI
        else:
            ret = None
        return ret

    def addItem(self, imgEntry):
        self.persistToStore([imgEntry])
        self._items[imgEntry._imgId] = imgEntry

    def updateItem(self, imgId, imgEntry):
        ret = True
        if imgId not in self._items.keys():
            ret = False
        else:
            self._items[imgEntry._imgId] = imgEntry
        return ret

    def queryStore(self, imgIds):
        ret = False
        self._getItems()
        if not isinstance(imgIds, list):
            if imgIds in self._items.keys():
                ret = True
                ret = self._items[imgIds]
        return ret

    def _getItems(self):
        f = open(self._fsloc, 'r')
        self._items.clear()
        items = f.readlines()
        for item in items:
            item = eval(item)
            segs = item.split(',')
            args = [ x.strip() for x in segs ]
            self._items[args[0]] = ImgEntry(args[0], None, args[1])

        f.close()
        return

    def persistToStore(self, items):
        f = open(self._fsloc, 'a')
        for item in items:
            f.write(str(item) + '\n')

        f.close()


class ImgMetaStoreFS(AbstractImgMetaStore):

    def __init__(self):
        super(ImgMetaStoreFS, self).__init__()
        self._fsloc = 'IRMetaStore'

    def getItem(self, imgId):
        if imgId not in self._items.keys():
            if self.queryStore('id=' + imgId):
                ret = self._items[imgId]
            else:
                ret = None
        else:
            ret = self._items[imgId]
        return ret

    def addItem(self, imgMeta):
        self.persistToStore([imgMeta])
        self._items[imgMeta._imgId] = imgMeta

    def updateItem(self, imgId, imgMeta):
        ret = True
        if imgId not in self._items.keys():
            ret = False
        else:
            self._items[imgMeta._imgId] = imgMeta
        return ret

    def getItems(self, criteria):
        if self.queryStore(criteria):
            return self._items
        else:
            return
            return

    def queryStore(self, criteria):
        ret = False
        self._items.clear()
        f = open(self._fsloc, 'r')
        items = f.readlines()
        if criteria == '*':
            for item in items:
                item = eval(item)
                segs = item.split(',')
                args = [ x.strip() for x in segs ]
                tmpMeta = ImgMeta(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9])
                self._items[tmpMeta._imgId] = tmpMeta

            ret = True
        elif re.findall('id=.+', criteria):
            matched = re.search('id=.+', criteria).group[0]
            idsearched = matched.split('=')[1]
            for item in items:
                item = eval(item)
                segs = item.split(',')
                args = [ x.strip() for x in segs ]
                if args[0] == idsearched:
                    tmpMeta = ImgMeta(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9])
                    self._items[tmpMeta._imgId] = tmpMeta
                    ret = True
                    break

        else:
            print "query string not supported. Try '*'"
        f.close()
        return ret

    def persistToStore(self, items):
        f = open(self._fsloc, 'a')
        for item in items:
            f.write(str(item) + '\n')

        f.close()


class IRUserStoreFS(AbstractIRUserStore):
    """
    User store existing as a file or db
    """

    def __init__(self):
        super(IRUserStoreFS, self).__init__()
        self._fsloc = 'IRUserStore'

    def getUser(self, userId):
        """Get user from the store by Id"""
        return IRUser(userId)

    def addUser(self, user):
        pass

    def persistToStore(self, users):
        pass

    def uploadValidator(self, userId, imgSize):
        user = self.getUser(userId)
        ret = True
        if imgSize + user._fsUsed > user._fsCap:
            ret = False
        return ret