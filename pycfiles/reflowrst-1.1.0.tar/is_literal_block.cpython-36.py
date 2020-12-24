# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_literal_block.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 391 bytes


def is_literal_block(lines, index):
    if index == 0:
        return False
    else:
        if not lines[index].startswith(' '):
            return False
        else:
            if lines[(index - 1)] != '':
                return False
            current_index = index - 1
            while current_index > 0 and lines[current_index] == '':
                current_index -= 1

            if lines[current_index].endswith('::'):
                return True
        return False