# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ngergo/Workspaces/Nordcloud/ratatoskr/ratatoskr/operation_wrappers/base_wrappers.py
# Compiled at: 2019-03-20 07:33:15
# Size of source mod 2**32: 1723 bytes


class OperationWrapper:
    __doc__ = '\n        Base class that wraps functions and implements how to execute them.\n    '

    def __init__(self):
        pass

    def load_wrapped_operation(self, func):
        """
            Loads the wrapped operation into the OperationWrapper
            for later use.
        """
        self.wrapped_operation = func

    def get_wrapped_operation_name(self):
        """
            Returns the name (id) of the operation that was loaded
            into OperatioWrapper.
        """
        return self.wrapped_operation.__name__

    def help(self):
        """
            Method that returns documentation for the wrapped given function.
        """
        return self.wrapped_operation.__doc__

    def call(self, *args, **kwargs):
        """
            Method that implements the way of calling the wrapped function.

            @raises NotImplementedError if this function is notimplemented in the subclasses
        """
        raise NotImplementedError


class LocalOperation(OperationWrapper):
    __doc__ = '\n        Class to represent operations that must be executed on the host.\n    '

    def __init__(self, custom_name=str()):
        self.custom_name = custom_name

    def get_wrapped_operation_name(self):
        """
            Returns the name (id) of the operation that was loaded
            into OperatioWrapper.
        """
        if self.custom_name != '':
            return self.custom_name
        return self.wrapped_operation.__name__

    def call(self, *args, **kwargs):
        return (self.wrapped_operation)(*args, **kwargs)


class RemoteOperation(OperationWrapper):
    __doc__ = '\n        Base class to represent operations that must be executed on remote hosts.\n    '