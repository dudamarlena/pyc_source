# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/local/cli_common/user_exceptions.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 1305 bytes
"""
Class containing error conditions that are exposed to the user.
"""
from samcli.commands.exceptions import UserException

class InvokeContextException(UserException):
    __doc__ = '\n    Something went wrong invoking the function.\n    '


class InvalidSamTemplateException(UserException):
    __doc__ = '\n    The template provided was invalid and not able to transform into a Standard CloudFormation Template\n    '


class SamTemplateNotFoundException(UserException):
    __doc__ = '\n    The SAM Template provided could not be found\n    '


class DebugContextException(UserException):
    __doc__ = '\n    Something went wrong when creating the DebugContext\n    '


class ImageBuildException(UserException):
    __doc__ = '\n    Image failed to build\n    '


class CredentialsRequired(UserException):
    __doc__ = '\n    Credentials were not given when Required\n    '


class ResourceNotFound(UserException):
    __doc__ = '\n    The Resource requested was not found\n    '


class InvalidLayerVersionArn(UserException):
    __doc__ = '\n    The LayerVersion Arn given in the template is Invalid\n    '


class UnsupportedIntrinsic(UserException):
    __doc__ = '\n    Value from a template has an Intrinsic that is unsupported\n    '


class NotAvailableInRegion(UserException):
    __doc__ = '\n    Calling service not available (launched) in specified region\n    '