# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/drf-batch-requests/drf_batch_requests/exceptions.py
# Compiled at: 2018-02-19 03:35:34
# Size of source mod 2**32: 168 bytes


class BatchRequestException(Exception):
    pass


class RequestAttributeError(BatchRequestException):
    __doc__ = ' Empty request attribute. Unable to perform request.  '