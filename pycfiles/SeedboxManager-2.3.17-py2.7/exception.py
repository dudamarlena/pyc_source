# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/db/exception.py
# Compiled at: 2015-06-14 13:30:57
"""
Database Exception definition classes
"""
import six

class DBError(Exception):
    """Wraps an implementation specific exception."""

    def __init__(self, inner_exception=None):
        self.inner_exception = inner_exception
        super(DBError, self).__init__(six.text_type(inner_exception))


class MultipleResultsFound(DBError):
    """Represents when Multiple results found when searching by unique id"""
    pass


class NoResultFound(DBError):
    """Represents when No results found when fetching by unique id"""
    pass


class DbMigrationError(DBError):
    """Wraps migration specific exception."""

    def __init__(self, message=None):
        super(DbMigrationError, self).__init__(message)