# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/comicnamer/comicnamer_exceptions.py
# Compiled at: 2010-09-01 08:38:12
__doc__ = 'Exceptions used through-out comicnamer\nModified from http://github.com/dbr/tvnamer\n'

class BaseComicnamerException(Exception):
    """Base exception all comicnamers exceptions inherit from
    """


class InvalidPath(BaseComicnamerException):
    """Raised when an argument is a non-existent file or directory path
    """


class NoValidFilesFoundError(BaseComicnamerException):
    """Raised when no valid files are found. Effectively exits tvnamer
    """


class InvalidFilename(BaseComicnamerException):
    """Raised when a file is parsed, but no issue info can be found
    """


class UserAbort(BaseComicnamerException):
    """Base exception for config errors
    """


class BaseConfigError(BaseComicnamerException):
    """Base exception for config errors
    """


class ConfigValueError(BaseConfigError):
    """Raised if the config file is malformed or unreadable
    """


class DataRetrievalError(BaseComicnamerException):
    """Raised when an error (such as a network problem) prevents comicnamer
    from being able to retrieve data such as issue name
    """


class SeriesNotFound(DataRetrievalError):
    """Raised when a series cannot be found
    """


class IssueNotFound(DataRetrievalError):
    """Raised when issue cannot be found
    """


class IssueNameNotFound(DataRetrievalError):
    """Raised when the name of the issue cannot be found
    """