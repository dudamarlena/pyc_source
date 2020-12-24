# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/influxable/helpers/utils.py
# Compiled at: 2019-09-20 05:34:14
# Size of source mod 2**32: 39 bytes


def inv(x):
    if x:
        return 1 / x
    return 0