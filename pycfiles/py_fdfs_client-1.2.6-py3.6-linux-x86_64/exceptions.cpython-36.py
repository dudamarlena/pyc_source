# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fdfs_client/exceptions.py
# Compiled at: 2018-11-05 04:52:27
# Size of source mod 2**32: 324 bytes
"""Core exceptions raised by fdfs client"""

class FDFSError(Exception):
    pass


class ConnectionError(FDFSError):
    pass


class ResponseError(FDFSError):
    pass


class InvaildResponse(FDFSError):
    pass


class DataError(FDFSError):
    pass