# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ewheeler/dev/pygrowup/pygrowup/exceptions.py
# Compiled at: 2013-10-18 23:16:24
# Size of source mod 2**32: 179 bytes


class DataNotFound(RuntimeError):
    pass


class DataError(RuntimeError):
    pass


class InvalidAge(RuntimeError):
    pass


class InvalidMeasurement(RuntimeError):
    pass