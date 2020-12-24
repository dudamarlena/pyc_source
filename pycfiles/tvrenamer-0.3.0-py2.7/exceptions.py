# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/exceptions.py
# Compiled at: 2015-11-08 18:30:19
"""Exceptions used through-out tvrenamer."""

class BaseTvRenamerException(Exception):
    """Base exception all tvrenamers exceptions inherit from."""
    pass


class InvalidFilename(BaseTvRenamerException):
    """Raised when a file is parsed, but no episode info can be found."""
    pass


class ConfigValueError(BaseTvRenamerException):
    """Raised if the config file is malformed or unreadable."""
    pass


class DataRetrievalError(BaseTvRenamerException):
    """Raised when unable to retrieve data.

    An error (such as a network problem) prevents tvrenamer
    from being able to retrieve data such as episode name
    """
    pass


class ShowNotFound(DataRetrievalError):
    """Raised when a show cannot be found."""
    pass


class SeasonNotFound(DataRetrievalError):
    """Raised when requested season cannot be found."""
    pass


class EpisodeNotFound(DataRetrievalError):
    """Raised when episode cannot be found."""
    pass