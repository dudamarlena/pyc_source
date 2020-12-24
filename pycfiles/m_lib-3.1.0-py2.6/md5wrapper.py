# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/md5wrapper.py
# Compiled at: 2016-07-25 14:36:49
"""User wrapper for md5 builtin object"""
from __future__ import print_function
import sys
if sys.version < '2.5':
    from md5 import md5
else:
    from hashlib import md5
__all__ = [
 'md5wrapper']

class md5wrapper:

    def __init__(self, init=None):
        if init:
            if not isinstance(init, bytes):
                init = init.encode('ascii')
            self._md5 = md5(init)
        else:
            self._md5 = md5()

    def update(self, data):
        self._md5.update(data)

    def digest(self):
        return self._md5.digest()

    def __repr__(self):
        str = self.digest()
        if isinstance(str, bytes):
            str = str.decode('latin1')
        return '%02x' * len(str) % tuple(map(ord, str))

    def md5file(self, f):
        if type(f) == type(''):
            infile = open(f, 'r')
        else:
            infile = f
        try:
            while 1:
                buf = infile.read(16384)
                if not buf:
                    break
                self.update(buf)

        finally:
            if type(f) == type(''):
                infile.close()


if __name__ == '__main__':
    print('This must print exactly the string')
    print('Test: 900150983cd24fb0d6963f7d28e17f72')
    print('Test:', md5wrapper('abc'))