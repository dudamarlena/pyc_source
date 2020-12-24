# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/core/exception.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

class SqlmapBaseException(Exception):
    pass


class SqlmapCompressionException(SqlmapBaseException):
    pass


class SqlmapConnectionException(SqlmapBaseException):
    pass


class SqlmapDataException(SqlmapBaseException):
    pass


class SqlmapFilePathException(SqlmapBaseException):
    pass


class SqlmapGenericException(SqlmapBaseException):
    pass


class SqlmapMissingDependence(SqlmapBaseException):
    pass


class SqlmapMissingMandatoryOptionException(SqlmapBaseException):
    pass


class SqlmapMissingPrivileges(SqlmapBaseException):
    pass


class SqlmapNoneDataException(SqlmapBaseException):
    pass


class SqlmapNotVulnerableException(SqlmapBaseException):
    pass


class SqlmapSilentQuitException(SqlmapBaseException):
    pass


class SqlmapUserQuitException(SqlmapBaseException):
    pass


class SqlmapSyntaxException(SqlmapBaseException):
    pass


class SqlmapThreadException(SqlmapBaseException):
    pass


class SqlmapUndefinedMethod(SqlmapBaseException):
    pass


class SqlmapUnsupportedDBMSException(SqlmapBaseException):
    pass


class SqlmapUnsupportedFeatureException(SqlmapBaseException):
    pass


class SqlmapValueException(SqlmapBaseException):
    pass