# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_directive.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 289 bytes


def is_directive(lines, index):
    """check if the line contains a directive"""
    if lines[index].lstrip().startswith('.. '):
        if '::' in lines[index]:
            return True
    if lines[index].lstrip().startswith('.. _'):
        return True
    else:
        return False