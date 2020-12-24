# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/pyawsbuckets/exceptions.py
# Compiled at: 2013-05-20 09:14:00


class AwsError(Exception):
    """Base error class."""


class AwsRequestFailureError(AwsError):
    """A packaged request was met with an unexpected response."""