# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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