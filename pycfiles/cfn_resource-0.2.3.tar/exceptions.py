# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cfn_pyplates/exceptions.py
# Compiled at: 2014-08-17 18:06:46


class Error(Exception):
    """Base exception class for cfn_pyplates

    A namespaced Exception subclass with explicit 'message' support.
    Will be handled at template generation, with the message being delivered
    to the user.

    Args:
        message: An optional message to package with the Error
        args: Any number of optional arguments, to be used as subclasses
            see fit.

    """
    message = 'An unknown error has occurred.'

    def __init__(self, message=None, *args):
        if not message:
            message = self.message
        else:
            self.message = message
        self.args = (
         message,) + args


class AddRemoveError(Error):
    """Raised when attempting to attach weird things to a JSONableDict

    Weird things, in this case, mean anything that isn't a JSONableDict

    Args:
        message: An optional message to package with the Error

    """
    message = 'Only subclasses of JSONableDict can be added or removed'


class IntrinsicFuncInputError(Error):
    """Raised when passing bad input values to an intrinsic function

    Args:
        message: An optional message to package with the Error

    """
    message = 'Invalid arguments passed to intrinsic function'