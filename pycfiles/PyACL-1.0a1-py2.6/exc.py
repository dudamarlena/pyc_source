# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/acl/exc.py
# Compiled at: 2009-04-27 10:20:36
"""
PyACL exceptions.

"""

class PyACLException(Exception):
    """Base class for the exceptions raised by PyACL and its plugins."""
    pass


class ExistingACOError(PyACLException):
    """
    Exception raised when trying to add an existing subresource or operation
    in a resource.
    
    """
    pass


class NoACOMatchError(PyACLException):
    """
    Exception raised when a non-existing subresource or operation is requested
    to a resource.
    
    """
    pass


class AdapterError(PyACLException):
    """Base exception for problems the source adapters."""
    pass


class SourceError(AdapterError):
    """
    Exception for problems with the source itself.
    
    .. attention::
        If you are creating a :term:`source adapter`, this is the only
        exception you should raise.
    
    """
    pass


class ExistingGroupError(AdapterError):
    """Exception raised when trying to add an existing group."""
    pass


class NonExistingGroupError(AdapterError):
    """Exception raised when trying to use a non-existing group."""
    pass


class UserPresentError(AdapterError):
    """
    Exception raised when trying to add a user to a group that already
    contains it.
    
    """
    pass


class UserNotPresentError(AdapterError):
    """
    Exception raised when trying to remove a user from a group that 
    doesn't contain it.
    
    """
    pass