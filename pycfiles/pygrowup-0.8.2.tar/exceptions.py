# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pygrowup/exceptions.py
# Compiled at: 2013-10-18 23:16:24


class DataNotFound(RuntimeError):
    pass


class DataError(RuntimeError):
    pass


class InvalidAge(RuntimeError):
    pass


class InvalidMeasurement(RuntimeError):
    pass