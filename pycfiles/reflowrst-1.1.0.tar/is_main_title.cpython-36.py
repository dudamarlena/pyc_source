# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_main_title.py
# Compiled at: 2018-03-08 13:43:31
# Size of source mod 2**32: 551 bytes
from .tools import is_only

def is_main_title(lines, index):
    """
    Determine if the lines follow the format of a main title
    """
    if index > len(lines) - 3:
        return False
    else:
        if len(lines[index]) == 0:
            return False
        symbol = lines[index][0]
        if is_only(lines[index].strip(), [symbol]):
            if is_only(lines[(index + 2)].strip(), [symbol]):
                if len(lines[index]) >= len(lines[(index + 1)]):
                    if len(lines[(index + 2)]) >= len(lines[(index + 1)]):
                        return True
        return False