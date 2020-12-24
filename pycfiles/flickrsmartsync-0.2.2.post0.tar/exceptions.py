# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/faisal/Developer/Projects/github/flickrsmartsync/flickrapi/exceptions.py
# Compiled at: 2014-06-18 08:36:36
"""Exceptions used by the FlickrAPI module."""

class IllegalArgumentException(ValueError):
    """Raised when a method is passed an illegal argument.

    More specific details will be included in the exception message
    when thrown.
    """
    pass


class FlickrError(Exception):
    """Raised when a Flickr method fails.

    More specific details will be included in the exception message
    when thrown.
    """
    pass


class CancelUpload(Exception):
    """Raise this exception in an upload/replace callback function to
    abort the upload.
    """
    pass


class LockingError(Exception):
    """Raised when TokenCache cannot acquire a lock within the timeout
    period, or when a lock release is attempted when the lock does not
    belong to this process.
    """
    pass