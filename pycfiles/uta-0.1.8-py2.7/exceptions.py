# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uta/exceptions.py
# Compiled at: 2014-08-27 16:21:43


class UTAError(Exception):
    pass


class DatabaseError(UTAError):
    pass


class InvalidTranscriptError(UTAError):
    pass


class InvalidIntervalError(UTAError):
    pass


class InvalidHGVSVariantError(UTAError):
    pass