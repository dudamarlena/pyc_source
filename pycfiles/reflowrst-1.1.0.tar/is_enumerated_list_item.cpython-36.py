# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_enumerated_list_item.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 723 bytes
from .tools import fromRoman

def is_enumerated_list_item(lines, index):
    """Check if it's an enumerated list item"""
    if len(lines[index].lstrip()) == 0:
        return False
    else:
        enumerator = lines[index].lstrip().split(' ')[0]
        if not enumerator.endswith('.'):
            if not enumerator.endswith(')'):
                return False
        enumerator = enumerator[0:-1]
        if enumerator.startswith('('):
            enumerator = enumerator[1:]
        try:
            int(enumerator)
            return True
        except:
            try:
                fromRoman(enumerator)
                return True
            except:
                if len(enumerator) == 1:
                    if enumerator.isalpha():
                        return True
                return False