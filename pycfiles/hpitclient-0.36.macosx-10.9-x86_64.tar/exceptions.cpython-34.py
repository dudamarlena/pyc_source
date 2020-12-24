# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Projects/TutorGen/python-client/env/lib/python3.4/site-packages/hpitclient/exceptions.py
# Compiled at: 2014-11-13 10:36:54
# Size of source mod 2**32: 1439 bytes


class ConnectionError(Exception):
    __doc__ = '\n    This exception indicates a generic HPIT connection problem.\n    '


class AuthenticationError(Exception):
    __doc__ = '\n    This exception raised on HPIT 403.\n    '


class AuthorizationError(Exception):
    __doc__ = "\n    This exception is raised when you've made an authorization grant request\n    when you are not the owner of the message type or resource.\n    "


class ResourceNotFoundError(Exception):
    __doc__ = '\n    This exception raised on HPIT 403.\n    '


class InternalServerError(Exception):
    __doc__ = '\n    This exception raised on HPIT 500.\n    '


class PluginRegistrationError(Exception):
    __doc__ = '\n    This exception indicates that a plugin could not register with HPIT.\n    '


class PluginPollError(Exception):
    __doc__ = '\n    This exception indicates that a plugin could not poll HPIT.\n    '


class ResponseDispatchError(Exception):
    __doc__ = '\n    This exception indicates that a response from HPIT could not be dispatched to a callback.\n    '


class InvalidMessageNameException(Exception):
    __doc__ = "\n    This exception is raised when a user attempts to use a system message name, like 'transaction'.\n    "


class InvalidParametersError(Exception):
    __doc__ = "\n    You haven't met the requirements for this function.\n    "


class BadCallbackException(Exception):
    __doc__ = '\n    Raised when a callback is not callable\n    '