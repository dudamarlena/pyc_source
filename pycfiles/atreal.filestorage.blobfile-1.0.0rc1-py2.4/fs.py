# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/filestorage/blobfile/fs.py
# Compiled at: 2009-09-18 09:19:43
import os, tempfile
from StringIO import StringIO
from zope.interface import implements
from Products.blob.zopefile import OFSBlobFile
from atreal.filestorage.common.zodbstore import ZodbFile, ZodbDir
from atreal.filestorage.common.interfaces import IOmniFile

class BlobFile(ZodbFile):
    __module__ = __name__

    def __init__(self, name, parent, wrapFile=None):
        if wrapFile is None:
            wrapFile = OFSBlobFile('', '', StringIO())
        ZodbFile.__init__(self, name, parent, wrapFile)
        return

    def open(self, mode='r'):
        return self.data.data.open(mode)

    def displaceOnFS(self):
        self.lock = True
        (fd, self.onFS) = tempfile.mkstemp(suffix=self.name)
        fs_file = os.fdopen(fd, 'w')
        file_obj = self.data.data.open('r')
        for chunk in file_obj:
            fs_file.write(chunk)

        fs_file.close()
        return self.onFS


class OfsBlobToOmni(BlobFile):
    __module__ = __name__
    implements(IOmniFile)

    def __init__(self, blob_file):
        BlobFile.__init__(self, blob_file.filename, None, blob_file)
        return

    def setContentType(self, value):
        raise NotImplementedError

    def getContentType(self):
        return self.data.getContentType()


class BlobDir(ZodbDir):
    __module__ = __name__

    def makeFile(self, name):
        return self.makeChild(name, BlobFile)

    def makeDir(self, name):
        return self.makeChild(name, BlobDir)