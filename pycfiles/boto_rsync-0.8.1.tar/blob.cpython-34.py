# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sdb/db/blob.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2437 bytes
from boto.compat import six

class Blob(object):
    """Blob"""

    def __init__(self, value=None, file=None, id=None):
        self._file = file
        self.id = id
        self.value = value

    @property
    def file(self):
        from StringIO import StringIO
        if self._file:
            f = self._file
        else:
            f = StringIO(self.value)
        return f

    def __str__(self):
        return six.text_type(self).encode('utf-8')

    def __unicode__(self):
        if hasattr(self.file, 'get_contents_as_string'):
            value = self.file.get_contents_as_string()
        else:
            value = self.file.getvalue()
        if isinstance(value, six.text_type):
            return value
        else:
            return value.decode('utf-8')

    def read(self):
        if hasattr(self.file, 'get_contents_as_string'):
            return self.file.get_contents_as_string()
        else:
            return self.file.read()

    def readline(self):
        return self.file.readline()

    def next(self):
        return next(self.file)

    def __iter__(self):
        return iter(self.file)

    @property
    def size(self):
        if self._file:
            return self._file.size
        else:
            if self.value:
                return len(self.value)
            return 0