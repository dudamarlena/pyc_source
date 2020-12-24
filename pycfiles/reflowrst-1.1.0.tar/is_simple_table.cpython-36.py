# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_simple_table.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 566 bytes
from .tools import is_only

def is_simple_table(lines, index):
    """This algorithm requires that there be no blank lines inside your table"""
    current_index = index
    if is_only(lines[current_index], ['=', ' ']):
        count = 1
        top_line = lines[current_index]
        current_index += 1
        while current_index < len(lines) and not lines[current_index] == '':
            if lines[current_index] == top_line:
                count += 1
            current_index += 1

        if count == 3:
            return True
    else:
        return False