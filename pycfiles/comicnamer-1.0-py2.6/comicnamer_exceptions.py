# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/comicnamer/comicnamer_exceptions.py
# Compiled at: 2010-09-01 08:38:12
"""Exceptions used through-out comicnamer
Modified from http://github.com/dbr/tvnamer
"""

class BaseComicnamerException(Exception):
    """Base exception all comicnamers exceptions inherit from
    """
    pass


class InvalidPath(BaseComicnamerException):
    """Raised when an argument is a non-existent file or directory path
    """
    pass


class NoValidFilesFoundError(BaseComicnamerException):
    """Raised when no valid files are found. Effectively exits tvnamer
    """
    pass


class InvalidFilename(BaseComicnamerException):
    """Raised when a file is parsed, but no issue info can be found
    """
    pass


class UserAbort(BaseComicnamerException):
    """Base exception for config errors
    """
    pass


class BaseConfigError(BaseComicnamerException):
    """Base exception for config errors
    """
    pass


class ConfigValueError(BaseConfigError):
    """Raised if the config file is malformed or unreadable
    """
    pass


class DataRetrievalError(BaseComicnamerException):
    """Raised when an error (such as a network problem) prevents comicnamer
    from being able to retrieve data such as issue name
    """
    pass


class SeriesNotFound(DataRetrievalError):
    """Raised when a series cannot be found
    """
    pass


class IssueNotFound(DataRetrievalError):
    """Raised when issue cannot be found
    """
    pass


class IssueNameNotFound(DataRetrievalError):
    """Raised when the name of the issue cannot be found
    """
    pass