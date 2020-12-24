# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/stdplus/_fnmatches.py
# Compiled at: 2018-12-11 10:37:42
# Size of source mod 2**32: 169 bytes
from fnmatch import fnmatch

def fnmatches(string, patterns):
    for pattern in patterns:
        if fnmatch(string, pattern):
            return True

    return False