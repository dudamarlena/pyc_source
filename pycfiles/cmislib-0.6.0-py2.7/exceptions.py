# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/cmislib/exceptions.py
# Compiled at: 2017-08-27 12:31:07
"""
This module contains exceptions used throughout the API.
"""

class CmisException(Exception):
    """
    Common base class for all exceptions.
    """

    def __init__(self, status=None, url=None):
        Exception.__init__(self, 'Error %s at %s' % (status, url))
        self.status = status
        self.url = url


class InvalidArgumentException(CmisException):
    """ InvalidArgumentException """
    pass


class ObjectNotFoundException(CmisException):
    """ ObjectNotFoundException """
    pass


class NotSupportedException(CmisException):
    """ NotSupportedException """
    pass


class PermissionDeniedException(CmisException):
    """ PermissionDeniedException """
    pass


class RuntimeException(CmisException):
    """ RuntimeException """
    pass


class ConstraintException(CmisException):
    """ ConstraintException """
    pass


class ContentAlreadyExistsException(CmisException):
    """ContentAlreadyExistsException """
    pass


class FilterNotValidException(CmisException):
    """FilterNotValidException """
    pass


class NameConstraintViolationException(CmisException):
    """NameConstraintViolationException """
    pass


class StorageException(CmisException):
    """StorageException """
    pass


class StreamNotSupportedException(CmisException):
    """ StreamNotSupportedException """
    pass


class UpdateConflictException(CmisException):
    """ UpdateConflictException """
    pass


class VersioningException(CmisException):
    """ VersioningException """
    pass