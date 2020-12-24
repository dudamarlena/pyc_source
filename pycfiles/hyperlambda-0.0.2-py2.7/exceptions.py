# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hyperlambda/exceptions.py
# Compiled at: 2018-02-05 02:30:39
from __future__ import unicode_literals
import exceptions

class HyperLambdaError(Exception):
    """
    The base exception class for Hyperlambda exceptions.

    :ivar msg: The descriptive message associated with the error.
    """
    fmt = b'An unspecified error occurred'

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs


class NoFunctionError(HyperLambdaError):
    """No region was specified."""
    fmt = b'You must specify a Function_name.'


class InvalidTimeoutError(HyperLambdaError):
    """Invalid Timeout was specified."""
    fmt = b'You must specify a valid time in seconds.'


class NoHandlerError(HyperLambdaError):
    """No Handler was specified."""
    fmt = b'You must specify a handler name that need to be called.'


class NoScriptError(HyperLambdaError):
    """No script was specified."""
    fmt = b'You must specify a zip_file or code that need to be executed.'


class NoValidDictionaryError(HyperLambdaError):
    """No script was specified."""
    fmt = b'You must specify key-value pairs that represent your environment\'s configuration settings. eg: "{\'Variables\': {\'string\': \'string\'} }" '


class NoValidTagsDictionaryError(HyperLambdaError):
    fmt = b"You must specify key-value pairs that represent your tags's configuration settings. eg: {'string': 'string'} "


class NoValidDataTypeError(HyperLambdaError):
    fmt = b"You must specify a json dictionary that represent your data's configuration settings. "


class InstanceTerminatedError(HyperLambdaError):
    """No script was specified."""
    fmt = b"Instance Terminated. '{message}'"


class FunctionTimeoutError(HyperLambdaError):
    """No script was specified."""
    fmt = b"Task timed out after '{timeout}'' seconds"


class NoInstanceCreated(HyperLambdaError):
    fmt = b'{message}'


class NoFunctionError(HyperLambdaError):
    fmt = b"An error occurred when calling the describe_function operation. '{message}'"


class InvalidHandlerError(HyperLambdaError):
    fmt = b'The data given is not valid. '


class InvalidKeyNameTypeError(HyperLambdaError):
    fmt = b'KeyName should be of type string'


class InvalidSecurityGroupIdsTypeError(HyperLambdaError):
    fmt = b'SecurityGroupIds should be of type list'