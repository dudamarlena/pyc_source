# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/pyawsbuckets/exceptions.py
# Compiled at: 2013-05-20 09:14:00


class AwsError(Exception):
    """Base error class."""
    pass


class AwsRequestFailureError(AwsError):
    """A packaged request was met with an unexpected response."""
    pass