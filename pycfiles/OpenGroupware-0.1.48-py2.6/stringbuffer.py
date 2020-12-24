# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/plist/stringbuffer.py
# Compiled at: 2012-10-12 07:02:39
import StringIO

class StringBuffer:
    """
    A mutable string. This implementation is quite inefficient, but I doubt
    that implementing it with lists would be considerably faster.
    """

    def __init__(self):
        self._buffer = StringIO.StringIO('')

    def __str__(self):
        return self._buffer.getvalue()

    def __repr__(self):
        return repr(self.__str___())

    def __len__(self):
        return self._buffer.len

    def __hash__(self):
        return hash(self._buffer.getvalue())

    def clear(self):
        self._buffer = StringIO.StringIO('')

    def append(self, string):
        self._buffer.write(string)
        return
        self._buffer.write(repr(string).encode('utf-8'))