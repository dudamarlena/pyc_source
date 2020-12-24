# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/tools/get_field_name.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 290 bytes


def get_field_name(words):
    for x in range(len(words)):
        if words[x].endswith(':'):
            if not words[x].endswith('\\:'):
                field_name = ' '.join(words[0:x + 1])
                words = words[x + 1:]
                return (field_name, words)

    return (
     'collect_field.py: ERROR:', [])