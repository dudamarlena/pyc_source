# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/exceptions.py
# Compiled at: 2020-04-22 08:35:40
# Size of source mod 2**32: 4969 bytes
import warnings, typing as tp
__all__ = [
 'BaseSatellaError', 'ResourceLockingError', 'ResourceNotLocked', 'ResourceLocked',
 'ConfigurationValidationError', 'ConfigurationError', 'ConfigurationSchemaError',
 'PreconditionError', 'MetricAlreadyExists', 'BaseSatellaException', 'CustomException',
 'CodedCustomException', 'CodedCustomExceptionMetaclass', 'WouldWaitMore', 'LockIsHeld']

class CustomException(Exception):
    __doc__ = '"\n    Base class for your custom exceptions. It will:\n\n    1. Accept any number of arguments\n    2. Provide faithful __repr__ and a reasonable __str__\n\n    It passed all arguments that your exception received via super()\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args)
        self.kwargs = kwargs

    def __str__(self) -> str:
        a = '%s(%s' % (self.__class__.__qualname__.split('.')[(-1)], ', '.join(map(repr, self.args)))
        if self.kwargs:
            a += ', ' + ', '.join(map(lambda k, v: '%s=%s' % (k, repr(v)), self.kwargs.items()))
        a += ')'
        return a

    def __repr__(self) -> str:
        a = '%s%s(%s' % (
         self.__class__.__module__ + '.' if self.__class__.__module__ != 'builtins' else '',
         self.__class__.__qualname__,
         ', '.join(map(repr, self.args)))
        if self.kwargs:
            a += ', ' + ', '.join(map(lambda kv: '%s=%s' % (kv[0], repr(kv[1])), self.kwargs.items()))
        a += ')'
        return a


def get_base_of_bases(classes):
    class_bases = ()
    for class_ in classes:
        class_bases += class_.__bases__

    return class_bases


class CodedCustomExceptionMetaclass(type):
    __doc__ = '\n    Metaclass implementing the isinstance check for coded custom exceptions\n    '
    code = None

    def __instancecheck__(cls, instance):
        if super().__instancecheck__(instance):
            return True
        else:
            if cls is CodedCustomException:
                return super().__instancecheck__(instance)
            class_base = (cls,)
            while CodedCustomException not in get_base_of_bases(class_base) and class_base:
                class_base = get_base_of_bases(class_base)

            inst_base = (instance.__class__,)
            while CodedCustomException not in get_base_of_bases(inst_base) and inst_base:
                inst_base = get_base_of_bases(inst_base)

            if len(set(class_base).intersection(set(inst_base))) == 0:
                return False
        try:
            return cls.code == instance.code
        except AttributeError:
            return super().__instancecheck__(instance)


class CodedCustomException(CustomException, metaclass=CodedCustomExceptionMetaclass):

    def __init__(self, message, code=None, *args, **kwargs):
        (super().__init__)(message, code, *args, **kwargs)
        self.message = message
        if code is not None:
            self.code = code


class BaseSatellaError(CustomException):
    __doc__ = '"Base class for all Satella exceptions'


class BaseSatellaException(BaseSatellaError):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        warnings.warn('Use BaseSatellaError instead', DeprecationWarning)


class ResourceLockingError(BaseSatellaError):
    __doc__ = 'Base class for resource locking issues'


class ResourceLocked(ResourceLockingError):
    __doc__ = 'Given resource has been already locked'


class ResourceNotLocked(ResourceLockingError):
    __doc__ = 'Locking given resource is needed in order to access it'


class WouldWaitMore(ResourceLockingError):
    __doc__ = "wait()'s timeout has expired"


class PreconditionError(BaseSatellaError, ValueError):
    __doc__ = '\n    A precondition was not met for the argument\n    '


class ConfigurationError(BaseSatellaError):
    __doc__ = 'A generic error during configuration'


class ConfigurationSchemaError(ConfigurationError):
    __doc__ = 'Schema mismatch to what was seen'


class ConfigurationValidationError(ConfigurationSchemaError):
    __doc__ = 'A validator failed'

    def __init__(self, msg, value=None, **kwargs):
        """
        :param value: value found
        """
        (super().__init__)(msg, value, **kwargs)
        self.value = value


class MetricAlreadyExists(BaseSatellaError):
    __doc__ = 'Metric with given name already exists, but with a different type'

    def __init__(self, msg, name, requested_type, existing_type):
        super().__init__(msg)
        self.name = name
        self.requested_type = requested_type
        self.existing_type = existing_type


class LockIsHeld(ResourceLocked):
    __doc__ = '\n    An exception raised when lock is held by someone\n\n    :param pid: PID of the holder, who is alive at the time this exception was raised.\n        This is checked via psutil.\n    '

    def __init__(self, pid):
        self.pid = pid