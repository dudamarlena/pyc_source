# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/version.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1925 bytes
from distutils.version import LooseVersion

def _cmp(self, other):
    if isinstance(other, str):
        other = LooseVersion(other)
    else:
        stypes = map(lambda c: str if isinstance(c, str) else int, self.version)
        otypes = map(lambda c: str if isinstance(c, str) else int, other.version)
        for i, (stype, otype) in enumerate(zip(stypes, otypes)):
            if stype == str:
                if otype == int:
                    other.version[i] = str(other.version[i])
                if stype == int and otype == str:
                    self.version[i] = str(self.version[i])

        if self.version == other.version:
            return 0
        if self.version < other.version:
            return -1
        if self.version > other.version:
            return 1


LooseVersion._cmp = _cmp