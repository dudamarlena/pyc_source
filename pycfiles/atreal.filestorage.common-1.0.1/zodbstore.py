# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/romain/dev/buildouts/xnet4.1/src/atreal.filestorage.common/atreal/filestorage/common/zodbstore.py
# Compiled at: 2011-10-27 09:41:01
import os, tempfile
from StringIO import StringIO
from zope.interface import implements
from OFS.Image import File
from persistent import Persistent
from BTrees.OOBTree import OOBTree
from atreal.filestorage.common.interfaces import IOmniFile
from atreal.filestorage.common.registry import storage_classes

class _Marker(object):
    pass


class ZodbFileDesc(StringIO):
    filedata = None

    def __init__(self, filedata):
        self.filedata = filedata
        if isinstance(self.filedata.data, str):
            buffer = self.filedata.data
        else:
            buffer = []
            current = self.filedata.data
            while current is not None:
                buffer.append(current.data)
                current = current.next

            buffer = ('').join(buffer)
        StringIO.__init__(self, buffer)
        return

    def close(self):
        if self.closed:
            return
        else:
            self.seek(0)
            self.headers = dict()
            self.headers['content-type'] = self.filedata.getContentType()
            self.filedata.manage_upload(self)
            StringIO.close(self)
            self.filedata = None
            return

    def __del__(self):
        self.close()


class ZodbFile(Persistent):
    lock = False
    onFS = None
    _content_type = None
    implements(IOmniFile)

    def __init__(self, name, parent, wrapFile=None):
        self.name = name
        self.parent = parent
        if wrapFile is None:
            self.data = File('', '', StringIO())
        else:
            self.data = wrapFile
        return

    def open(self, mode='r'):
        if self.onFS:
            raise ''
        file_desc = ZodbFileDesc(self.data)
        return file_desc

    def displaceOnFS(self):
        self.lock = True
        (fd, self.onFS) = tempfile.mkstemp(suffix=self.name)
        fs_file = os.fdopen(fd, 'w')
        if isinstance(self.data.data, str):
            fs_file.write(self.data.data)
        else:
            current = self.data.data
            while current is not None:
                fs_file.write(current.data)
                current = current.next

            fs_file.close()
            return self.onFS

    def setContentType(self, value):
        self._content_type = value

    def getContentType(self):
        return self._content_type

    def discardFromFS(self):
        os.unlink(self.onFS)
        del self.onFS
        del self.lock

    def replaceFromFS(self):
        self.data.manage_upload(file(self.onFS))
        self.discardFromFS()


class OfsToOmni(ZodbFile):
    implements(IOmniFile)

    def __init__(self, ofs_file):
        ZodbFile.__init__(self, ofs_file.filename, None, ofs_file)
        return

    def setContentType(self, value):
        raise NotImplementedError

    def getContentType(self):
        return self.data.getContentType()


class ZodbDir(OOBTree):

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def makeChild(self, name, factory):
        if name in self:
            raise ''
        obj = factory(name, self)
        self[name] = obj
        return obj

    def makeFile(self, name):
        return self.makeChild(name, ZodbFile)

    def makeDir(self, name):
        return self.makeChild(name, ZodbDir)

    def getPath(self, path, default=_Marker):
        current = self
        for item in path.split('/'):
            if not isinstance(current, ZodbDir):
                raise ''
            if default is _Marker:
                current = current[item]
            else:
                current = current.get(item, default)
                if current is default:
                    return current

        return current

    def getOrMakeFile(self, path):
        current = self
        if '/' in path:
            (path, name) = path.rsplit('/', 1)
            for item in path.split('/'):
                if not isinstance(current, ZodbDir):
                    raise ''
                if item not in current:
                    current.makeDir('item')
                current = current[item]

        else:
            name = path
        if name in current:
            return current[name]
        else:
            return current.makeFile(name)


class ZodbStore(ZodbDir):
    title = 'Zodb File Store'

    def __init__(self, name, context):
        self.store_name = name
        self.context = context
        ZodbDir.__init__(self, '', None)
        return


storage_classes['zodb'] = ZodbStore