# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ngergo/Workspaces/Nordcloud/ratatoskr/ratatoskr/exceptions.py
# Compiled at: 2019-03-20 06:58:46
# Size of source mod 2**32: 612 bytes


class InvalidOperationWrapperError(Exception):
    __doc__ = '\n        Raised when the custom user-provided operation wrapper does\n        not meet some requirements.\n    '


class OperationAlreadyRegisteredError(Exception):
    __doc__ = '\n        Raised upon attempt to register an operation with a name that\n        is already present in the registry\n    '


class UnregisteredOperationError(Exception):
    __doc__ = '\n        Raised on dispatching event with unregistered oparation field\n    '


class SchemaValidationError(Exception):
    __doc__ = '\n        Raised on unmatching schema.\n    '