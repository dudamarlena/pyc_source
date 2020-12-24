# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ratatoskr/exceptions.py
# Compiled at: 2019-03-20 06:58:46


class InvalidOperationWrapperError(Exception):
    """
        Raised when the custom user-provided operation wrapper does
        not meet some requirements.
    """
    pass


class OperationAlreadyRegisteredError(Exception):
    """
        Raised upon attempt to register an operation with a name that
        is already present in the registry
    """
    pass


class UnregisteredOperationError(Exception):
    """
        Raised on dispatching event with unregistered oparation field
    """
    pass


class SchemaValidationError(Exception):
    """
        Raised on unmatching schema.
    """
    pass