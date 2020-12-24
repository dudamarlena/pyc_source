# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/exceptions.py
# Compiled at: 2018-05-03 13:55:55
from future.utils import raise_
from builtins import object
from contextlib import contextmanager
import sys

class panic(object):
    """
    The Python idiom for reraising a primary exception fails when the except block raises a
    secondary exception, e.g. while trying to cleanup. In that case the original exception is
    lost and the secondary exception is reraised. The solution seems to be to save the primary
    exception info as returned from sys.exc_info() and then reraise that.

    This is a contextmanager that should be used like this

    try:
         # do something that can fail
    except:
        with panic( log ):
            # do cleanup that can also fail

    If a logging logger is passed to panic(), any secondary Exception raised within the with
    block will be logged. Otherwise those exceptions are swallowed. At the end of the with block
    the primary exception will be reraised.
    """

    def __init__(self, log=None):
        super(panic, self).__init__()
        self.log = log
        self.exc_info = None
        return

    def __enter__(self):
        self.exc_info = sys.exc_info()

    def __exit__(self, *exc_info):
        if self.log is not None and exc_info and exc_info[0]:
            self.log.warn('Exception during panic', exc_info=exc_info)
        exc_type, exc_value, traceback = self.exc_info
        raise_(exc_type, exc_value, traceback)
        return


class RequirementError(Exception):
    """
    The expcetion raised bye require(). Where AssertionError is raised when there is likely an
    internal problem within the code base, i.e. a bug, an instance of this class is raised when
    the cause lies outside the code base, e.g. with the user or caller.
    """
    pass


def require(value, message, *message_args):
    """
    Raise RequirementError with the given message if the given value is considered false. See
    https://docs.python.org/2/library/stdtypes.html#truth-value-testing for a defintiion of which
    values are false. This function is commonly used for validating user input. It is meant to be
    complimentary to assert. See RequirementError for more on that.

    :param Any value: the value to be tested
    :param message:
    :param message_args: optional values for % formatting the given message
    :return:

    >>> require(1 + 1 == 2, 'You made a terrible mistake')

    >>> require(1 + 1 == 3, 'You made a terrible mistake')  # doctest: +IGNORE_EXCEPTION_DETAIL 
    Traceback (most recent call last):
    ...
    RequirementError: You made a terrible mistake

    >>> require(1 + 1 == 3, 'You made a terrible mistake, %s', 'you fool') # doctest: +IGNORE_EXCEPTION_DETAIL 
    Traceback (most recent call last):
    ...
    RequirementError: You made a terrible mistake, you fool

    >>> require(1 + 1 == 3, 'You made a terrible mistake, %s %s', 'your', 'majesty') # doctest: +IGNORE_EXCEPTION_DETAIL 
    Traceback (most recent call last):
    ...
    RequirementError: You made a terrible mistake, your majesty
    """
    if not value:
        if message_args:
            message = message % message_args
        raise RequirementError(message)