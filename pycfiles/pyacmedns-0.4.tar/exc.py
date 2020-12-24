# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/acl/exc.py
# Compiled at: 2009-04-27 10:20:36
__doc__ = '\nPyACL exceptions.\n\n'

class PyACLException(Exception):
    """Base class for the exceptions raised by PyACL and its plugins."""


class ExistingACOError(PyACLException):
    """
    Exception raised when trying to add an existing subresource or operation
    in a resource.
    
    """


class NoACOMatchError(PyACLException):
    """
    Exception raised when a non-existing subresource or operation is requested
    to a resource.
    
    """


class AdapterError(PyACLException):
    """Base exception for problems the source adapters."""


class SourceError(AdapterError):
    """
    Exception for problems with the source itself.
    
    .. attention::
        If you are creating a :term:`source adapter`, this is the only
        exception you should raise.
    
    """


class ExistingGroupError(AdapterError):
    """Exception raised when trying to add an existing group."""


class NonExistingGroupError(AdapterError):
    """Exception raised when trying to use a non-existing group."""


class UserPresentError(AdapterError):
    """
    Exception raised when trying to add a user to a group that already
    contains it.
    
    """


class UserNotPresentError(AdapterError):
    """
    Exception raised when trying to remove a user from a group that 
    doesn't contain it.
    
    """