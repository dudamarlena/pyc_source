# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/SyntheticUploadedFile.py
# Compiled at: 2010-03-05 03:20:49
from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
import os

class SyntheticUploadedFile(UploadedFile):
    """
    An 'fake' uploaded file, used to programmatically assign FileField (or ImageField)
    fields in model instances.
    """
    __module__ = __name__
    DEFAULT_CHUNK_SIZE = File.DEFAULT_CHUNK_SIZE

    def __init__(self, file_or_pathname, name=None, field_name=None, content_type=None, size=None, charset=None):
        if name is None:
            if isinstance(file_or_pathname, basestring):
                name = os.path.basename(file_or_pathname)
            else:
                name = file_or_pathname.name
        content_type = content_type or 'application/octet-stream'
        super(SyntheticUploadedFile, self).__init__(name, content_type, size, charset)
        if isinstance(file_or_pathname, basestring):
            self._path = file_or_pathname
            self._file = open(file_or_pathname, 'rb')
        else:
            self._path = None
            self._file = file_or_pathname
            self._file.seek(0)
        self.file = self._file
        self._name = self._file.name
        self._mode = self._file.mode
        self._closed = False
        self.field_name = field_name
        if size is None or size < 0:
            self._file.seek(0, os.SEEK_END)
            self._size = self._file.tell()
            self._file.seek(0)
        else:
            self._size = size
        return

    def __del__(self):
        if not self._closed:
            self.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self._closed:
            self.close()

    @property
    def path(self):
        return self._path

    def open(self):
        self._file.seek(0)

    def close(self):
        rv = self._file.close()
        self._closed = True
        return rv

    def chunks(self, chunk_size=None):
        if not chunk_size:
            chunk_size = self.DEFAULT_CHUNK_SIZE
        self.seek(0)
        counter = self.size
        while counter > 0:
            try:
                chunk = self.read(chunk_size)
            except Exception, exc:
                raise exc

            yield chunk
            counter -= len(chunk)

    def read(self, *args):
        return self._file.read(*args)

    def seek(self, *args):
        return self._file.seek(*args)

    def write(self, s):
        return self._file.write(s)

    def tell(self, *args):
        return self._file.tell(*args)

    def __iter__(self):
        return iter(self._file)

    def readlines(self, size=None):
        return self._file.readlines(size)

    def xreadlines(self):
        return self._file.xreadlines()