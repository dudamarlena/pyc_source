# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kinesis/exceptions.py
# Compiled at: 2019-05-20 19:30:35
# Size of source mod 2**32: 275 bytes


class StreamExists(Exception):
    pass


class StreamDoesNotExist(Exception):
    pass


class StreamShardLimit(Exception):
    pass


class StreamStatusInvalid(Exception):
    pass


class ExceededPutLimit(Exception):
    pass


class UnknownException(Exception):
    pass