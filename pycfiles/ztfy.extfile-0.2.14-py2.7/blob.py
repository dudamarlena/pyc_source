# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/extfile/blob.py
# Compiled at: 2014-11-13 09:53:29
__docformat__ = 'restructuredtext'
import os
from cStringIO import StringIO
from zope.container.interfaces import IContained
from ztfy.extfile.interfaces import IBaseBlobFile, IBlobFile, IBlobImage
from ZODB.blob import Blob
from zope.app.file.file import File
from zope.app.file.image import Image, getImageInfo
from zope.interface import implements
from ztfy.extfile import getMagicContentType
BLOCK_SIZE = 65536

class BaseBlobFile(File):
    """A persistent content class handling data stored in an external blob"""
    implements(IBaseBlobFile, IContained)

    def __init__(self, data='', contentType='', source=None):
        self.__parent__ = self.__name__ = None
        self.contentType = contentType
        self._blob = None
        if data:
            self.data = data
        elif source:
            if os.path.exists(source):
                try:
                    f = open(source, 'rb')
                    self.data = f.read()
                finally:
                    f.close()

        return

    def getBlob(self, mode='r'):
        if self._blob is None:
            return
        else:
            return self._blob.open(mode=mode)

    def _getData(self):
        f = self.getBlob()
        if f is None:
            return
        else:
            try:
                data = f.read()
                return data
            finally:
                f.close()

            return

    def _setData(self, data):
        if self._blob is None:
            self._blob = Blob()
        if isinstance(data, unicode):
            data = data.encode('UTF-8')
        f = self._blob.open('w')
        try:
            if hasattr(data, 'read'):
                self._size = 0
                _data = data.read(BLOCK_SIZE)
                size = len(_data)
                while size > 0:
                    f.write(_data)
                    self._size += size
                    _data = data.read(BLOCK_SIZE)
                    size = len(_data)

            else:
                f.write(data)
                self._size = len(data)
        finally:
            f.close()

        return

    data = property(_getData, _setData)

    def getSize(self):
        return self._size

    def __nonzero__(self):
        return self._size > 0


class BlobFile(BaseBlobFile):
    """Content class for BLOB files"""
    implements(IBlobFile)


class BlobImage(BaseBlobFile, Image):
    """Content class for BLOB images"""
    implements(IBlobImage)

    def _setData(self, data):
        BaseBlobFile._setData(self, data)
        contentType, self._width, self._height = getImageInfo(data)
        if contentType:
            self.contentType = contentType
        if self._width < 0 or self._height < 0:
            contentType = getMagicContentType(data)
            if contentType.startswith('image/'):
                try:
                    from PIL import Image
                    img = Image.open(StringIO(data))
                    self.contentType = contentType
                    self._width, self._height = img.size
                except (IOError, ImportError):
                    pass

    data = property(BaseBlobFile._getData, _setData)