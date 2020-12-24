# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_title.py
# Compiled at: 2018-03-08 13:50:11
# Size of source mod 2**32: 410 bytes
from .tools.is_only import is_only

def is_title(lines, index):
    """check to see if the line is a title"""
    if index > len(lines) - 2:
        return False
    else:
        if len(lines[(index + 1)]) == 0:
            return False
        symbol = lines[(index + 1)].strip()[0]
        if is_only(lines[(index + 1)].strip(), [symbol]):
            if len(lines[index]) <= len(lines[(index + 1)]):
                return True
        return False