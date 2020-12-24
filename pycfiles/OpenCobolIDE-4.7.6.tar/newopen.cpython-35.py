# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/types/newopen.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 811 bytes
"""
A substitute for the Python 3 open() function.

Note that io.open() is more complete but maybe slower. Even so, the
completeness may be a better default. TODO: compare these
"""
_builtin_open = open

class newopen(object):
    __doc__ = "Wrapper providing key part of Python 3 open() interface.\n\n    From IPython's py3compat.py module. License: BSD.\n    "

    def __init__(self, fname, mode='r', encoding='utf-8'):
        self.f = _builtin_open(fname, mode)
        self.enc = encoding

    def write(self, s):
        return self.f.write(s.encode(self.enc))

    def read(self, size=-1):
        return self.f.read(size).decode(self.enc)

    def close(self):
        return self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.f.close()