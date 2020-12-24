# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/errors.py
# Compiled at: 2016-03-23 14:50:19


class WintxError(Exception):
    """Base error class for Wintx errors"""
    pass


class WintxConfigError(WintxError):
    """Error class handling configuration errors"""
    pass


class WintxDatabaseError(WintxError):
    """Error class handling database errors"""
    pass


class WintxDriverError(WintxError):
    """Error class handling driver errors"""
    pass


class WintxFunctionNotImplemented(WintxDriverError):
    """Error class handling functions not supported by a driver"""
    pass


class WintxUserError(WintxError):
    """Error class handling user based errors"""
    pass


class WintxMalformedPolygonError(WintxUserError):
    """Error class handling malformed polygons"""
    pass


class WintxMalformedQueryError(WintxUserError):
    """Error class handling malformed queries"""
    pass


class WintxMalformedRecordError(WintxUserError):
    """Error class handling malformed records"""
    pass


class WintxMalformedSortError(WintxUserError):
    """Error class handling malformed sort lists"""
    pass


class WintxImportError(WintxError):
    """Error class handling import issues"""
    pass