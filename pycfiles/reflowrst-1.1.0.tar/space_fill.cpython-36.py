# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/tools/space_fill.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 161 bytes


def space_fill(count, symbol):
    """makes a string that is count long of symbol"""
    x = ''
    for i in range(0, count):
        x = x + symbol

    return x