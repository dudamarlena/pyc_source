# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komparse\char_stream.py
# Compiled at: 2020-03-07 08:14:04
# Size of source mod 2**32: 629 bytes


class CharStream(object):

    def open(self):
        pass

    def close(self):
        pass

    def has_next(self):
        return False

    def peek(self):
        pass

    def advance(self):
        pass


class StringStream(CharStream):

    def __init__(self, s):
        self._s = s
        self._idx = 0

    def has_next(self):
        return self._idx < len(self._s)

    def peek(self):
        return self._s[self._idx]

    def advance(self):
        ret = self._s[self._idx]
        self._idx += 1
        return ret