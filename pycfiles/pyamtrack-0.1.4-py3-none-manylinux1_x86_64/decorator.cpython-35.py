# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/decorator.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 2207 bytes
__doc__ = 'PyAMS_utils.decorator module\n\nThis module only provides a single decorator, which can be used to mark a function as\ndeprecated.\n'
import functools, warnings
__docformat__ = 'restructuredtext'

def deprecated(*msg):
    r"""This is a decorator which can be used to mark functions as deprecated.

    It will result in a warning being emitted when the function is used.

    >>> from pyams_utils.context import capture_stderr
    >>> from pyams_utils.decorator import deprecated

    >>> @deprecated
    ... def my_function(value):
    ...     return value

    >>> with capture_stderr(my_function, 1) as err:
    ...     print(err.split('\n')[0])
    <doctest ... DeprecationWarning: Function my_function is deprecated.

    >>> @deprecated('Deprecation message')
    ... def my_function_2(value):
    ...     return value

    >>> with capture_stderr(my_function_2, 2) as err:
    ...     print(err.split('\n')[0])
    <doctest ... DeprecationWarning: Function my_function_2 is deprecated. Deprecation message
    """

    def decorator(func):
        """Actual decorator"""

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            """Wrapped decorator function"""
            warnings.warn_explicit('Function %s is deprecated. %s' % (func.__name__, message), category=DeprecationWarning, filename=func.__code__.co_filename, lineno=func.__code__.co_firstlineno + 1)
            return func(*args, **kwargs)

        return new_func

    if len(msg) == 1 and callable(msg[0]):
        message = ''
        return decorator(msg[0])
    message = msg[0]
    return decorator