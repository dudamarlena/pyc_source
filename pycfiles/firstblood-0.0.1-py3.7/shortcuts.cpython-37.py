# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firstblood/unifiedIO/shortcuts.py
# Compiled at: 2018-10-28 13:45:36
# Size of source mod 2**32: 1436 bytes
import functools as fn
from math import inf
from .unified import Unified

def _shortcut(funcname, mode, ret):

    def inner(path, *args, **kwargs):
        with Unified(open(path, mode)) as (f):
            res = (getattr(f, funcname))(*args, **kwargs)
            if ret:
                return res

    inner.__name__ = funcname
    inner.__qualname__ = funcname
    return inner


read = _shortcut('read', 'r', True)
readline = _shortcut('readline', 'r', True)
readlines = _shortcut('readlines', 'r', True)
readuntil = _shortcut('readuntil', 'r', True)
write = _shortcut('write', 'w', False)
writeline = _shortcut('writeline', 'w', False)
writelines = _shortcut('writelines', 'w', False)
append = _shortcut('write', 'a', False)
appendline = _shortcut('writeline', 'a', False)
appendlines = _shortcut('writelines', 'a', False)
readbin = _shortcut('read', 'rb', True)
readbinline = _shortcut('readline', 'rb', True)
readbinlines = _shortcut('readlines', 'rb', True)
readbinuntil = _shortcut('readuntil', 'rb', True)
writebin = _shortcut('write', 'wb', False)
writebinline = _shortcut('writeline', 'wb', False)
writebinlines = _shortcut('writelines', 'wb', False)
appendbin = _shortcut('write', 'ab', False)
appendbinline = _shortcut('writeline', 'ab', False)
appendbinlines = _shortcut('writelines', 'ab', False)