# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/cmislib/exceptions.py
# Compiled at: 2017-08-27 12:31:07
__doc__ = '\nThis module contains exceptions used throughout the API.\n'

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


class ObjectNotFoundException(CmisException):
    """ ObjectNotFoundException """


class NotSupportedException(CmisException):
    """ NotSupportedException """


class PermissionDeniedException(CmisException):
    """ PermissionDeniedException """


class RuntimeException(CmisException):
    """ RuntimeException """


class ConstraintException(CmisException):
    """ ConstraintException """


class ContentAlreadyExistsException(CmisException):
    """ContentAlreadyExistsException """


class FilterNotValidException(CmisException):
    """FilterNotValidException """


class NameConstraintViolationException(CmisException):
    """NameConstraintViolationException """


class StorageException(CmisException):
    """StorageException """


class StreamNotSupportedException(CmisException):
    """ StreamNotSupportedException """


class UpdateConflictException(CmisException):
    """ UpdateConflictException """


class VersioningException(CmisException):
    """ VersioningException """