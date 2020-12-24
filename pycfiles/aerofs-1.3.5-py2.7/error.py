# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/error.py
# Compiled at: 2016-01-12 12:25:49


class APIException(Exception):
    pass


class NoRouteException(APIException):
    pass


class ReadOnlyException(APIException):
    pass


class WriteOnlyException(APIException):
    pass