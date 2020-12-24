# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_option_list_item.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 472 bytes


def is_option_list_item(lines, index):
    if not lines[index].startswith('-'):
        if not lines[index].startswith('/'):
            return False
    leading_space = lines[index].replace(lines[index].lstrip(), '')
    if '  ' not in lines[index]:
        if index < len(lines) - 1:
            if lines[(index + 1)].startswith(leading_space + ' '):
                return True
            else:
                return False
        else:
            return False
    return True