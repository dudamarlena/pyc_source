# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/sc/base/memberdataexport/streaming.py
# Compiled at: 2009-03-29 21:05:56
from ZPublisher.Iterators import IStreamIterator

class FileStreamer:
    """A mixin class which can be mixed in with a file or file-like class
    and implements an iterator that returns a fixed-sized sequence of bytes.
    """
    __module__ = __name__
    __implements__ = (
     IStreamIterator,)
    streamsize = 1 << 16

    def __init__(self, file):
        self._file = file

    def __getattr__(self, name):
        if self.__dict__.has_key(name):
            return self.__dict__[name]
        return getattr(self.__dict__['_file'], name)

    def next(self):
        data = self._file.read(self.streamsize)
        if not data:
            raise StopIteration
        return data

    def __nonzero__(self):
        return bool(self._file)

    def __len__(self):
        cur_pos = self._file.tell()
        self._file.seek(0, 2)
        size = self._file.tell()
        self._file.seek(cur_pos, 0)
        return int(size)