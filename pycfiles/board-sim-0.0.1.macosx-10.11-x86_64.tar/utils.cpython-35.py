# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/board-sim/core/utils.py
# Compiled at: 2016-09-10 17:13:22
# Size of source mod 2**32: 1453 bytes


def hasproperty(instance, property):
    try:
        if property in instance.properties:
            return True
        else:
            return False
    except AttributeError as tb:
        raise AttributeError('{} is not a valid BoardSim object'.format(type(instance))).with_traceback(tb.__traceback__)