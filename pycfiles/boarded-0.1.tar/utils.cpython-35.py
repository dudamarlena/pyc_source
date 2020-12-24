# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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