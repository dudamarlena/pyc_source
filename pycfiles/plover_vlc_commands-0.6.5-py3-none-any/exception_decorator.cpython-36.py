# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/vcs/exception_decorator.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 783 bytes
from plover_vcs.vcs.vcs_exception import VcsException
import inspect

def wrap_exceptions():
    """
    Decorator that wraps all methods of a class with
    the exception_decorator
    :return: decorator function
    """

    def decorate(cls):
        for name, fn in inspect.getmembers(cls, inspect.isfunction):
            setattr(cls, name, exception_decorator(fn))

        return cls

    return decorate


def exception_decorator(func):
    """
    Decorator that catches all exceptions and wraps them
    in the generic VcsException
    :param func: function to wrap
    :return: decorator function
    """

    def decorated(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            raise VcsException(e)

    return decorated