# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_field.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 431 bytes


def other_colon_present(words):
    for word in words:
        if word.endswith(':'):
            if not word.endswith('\\:'):
                return True

    return False


def is_field(lines, index):
    words = lines[index].lstrip().split(' ')
    if not words[0].startswith(':'):
        return False
    if not other_colon_present(words):
        return False
    else:
        if not words[0] == '::':
            return True
        return False