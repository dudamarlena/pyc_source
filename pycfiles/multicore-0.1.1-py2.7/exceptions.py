# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/multicore/exceptions.py
# Compiled at: 2017-08-13 05:19:27


class MulticoreError(Exception):
    pass


class TimeoutExceededError(MulticoreError):
    pass


class NoAvailableInputBufferError(MulticoreError):
    pass


class InputBufferTooSmallError(MulticoreError):
    pass


class TaskCompleteError(MulticoreError):
    pass