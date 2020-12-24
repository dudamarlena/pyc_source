# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../logomaker/src/error_handling.py
# Compiled at: 2019-04-11 12:38:45
# Size of source mod 2**32: 4390 bytes
from __future__ import division
from functools import wraps

class LogomakerError(Exception):
    __doc__ = '\n    Class used by Logomaker to handle errors.\n\n    parameters\n    ----------\n\n    message: (str)\n        The message passed to check(). This only gets passed to the\n        LogomakerError constructor when the condition passed to check() is\n        False.\n    '

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class DebugResult:
    __doc__ = '\n    Container class for debugging results.\n    '

    def __init__(self, result, mistake):
        self.result = result
        self.mistake = mistake


def check(condition, message):
    """
    Checks a condition; raises a LogomakerError with message if condition
    evaluates to False

    parameters
    ----------

    condition: (bool)
        A condition that, if false, halts Logomaker execution and raises a
        clean error to user

    message: (str)
        The string to show user if condition is False.

    returns
    -------
    None
    """
    if not condition:
        raise LogomakerError(message)


def handle_errors(func):
    """
    Decorator function to handle Logomaker errors.

    This decorator allows the user to pass the keyword argument
    'should_fail' to any wrapped function.

    If should_fail is None (or is not set by user), the function executes
    normally, and can be called as

        result = func(*args, **kwargs)

    In particular, Python execution will halt if any errors are raised.

    However, if the user specifies should_fail=True or should_fail=False, then
    Python will not halt even in the presence of an error. Moreover, the
    function will return a tuple, e.g.,

        result, mistake = func(*args, should_fail=True, **kwargs)

    with mistake flagging whether or not the function failed or succeeded
    as expected.
    """

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        should_fail = kwargs.pop('should_fail', None)
        check(should_fail in (True, False, None), 'FATAL: should_fail = %s is not bool or None' % should_fail)
        result = None
        mistake = None
        try:
            result = func(*args, **kwargs)
            if should_fail is True:
                print('UNEXPECTED SUCCESS.')
                mistake = True
            else:
                if should_fail is False:
                    print('Expected success.')
                    mistake = False
        except LogomakerError as e:
            if should_fail is True:
                print('Expected error:', e.__str__())
                mistake = False
            else:
                if should_fail is False:
                    print('UNEXPECTED ERROR:', e.__str__())
                    mistake = True
                else:
                    raise e

        if should_fail is None:
            return result
        else:
            if func.__name__ == '__init__':
                args[0].mistake = mistake
                return
            return DebugResult(result, mistake)

    return wrapped_func