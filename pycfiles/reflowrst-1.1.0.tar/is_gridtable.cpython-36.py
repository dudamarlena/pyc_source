# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_gridtable.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 254 bytes
from .tools import is_only

def is_gridtable(lines, i):
    if lines[i].lstrip().startswith('+-'):
        if lines[i].rstrip().endswith('-+'):
            if is_only(lines[i].strip(), ['+', '-', ' ']):
                return True
    return False