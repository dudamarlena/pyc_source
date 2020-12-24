# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/FBpyGIF/shuffle.py
# Compiled at: 2017-09-05 07:56:56
# Size of source mod 2**32: 233 bytes


def sfcycle(lst, nxt=0):
    from random import shuffle
    while True:
        half = len(lst) // 2
        last = lst[(-1)]
        remain = lst[:-1]
        shuffle(remain)
        lst = remain[:half] + [last] + remain[half:]
        for o in lst:
            yield o