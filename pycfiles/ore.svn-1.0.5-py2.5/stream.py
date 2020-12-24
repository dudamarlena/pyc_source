# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/stream.py
# Compiled at: 2008-05-07 15:44:29
"""
file handle abstraction for svn nodes
$Id: stream.py 2205 2008-05-07 19:44:27Z hazmat $
"""
from cStringIO import StringIO

class FileStream(object):

    def __init__(self, file, mode='r'):
        self.file = file
        self.stream = StringIO(file.contents)
        self.changed = False
        self.closed = False
        self.mode = mode

    def read(self, size=-1):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        return self.stream.read(size)

    def close(self):
        self.flush()
        self.closed = True
        self.node = None
        del self.stream
        return

    def seek(self, offset, whence=0):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        return self.stream.seek(offset, whence)

    def tell(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        return self.stream.tell()

    def flush(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        if self.changed:
            self.node.contents = self.stream.getvalue()
            self.changed = False

    def write(self, data):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        self.stream.write(data)