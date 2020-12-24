# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyquchk/qc_decorator.py
# Compiled at: 2013-09-22 13:33:06
from collections import OrderedDict
from functools import wraps
import inspect
from .checker import Checker
from .utils import optional_args

@optional_args
def qc(ntests=None, nshrinks=None, nassume=None):
    """ qc(ntests=None, nshrinks=None, nassume=None)
    Decorator for a test function.

    For usage examples see :ref:`creating-tests`.

    :param ntests: number of tests
    """
    frames = inspect.stack()
    func_is_method = any(fr[4][0].strip().startswith('class ') for fr in frames if fr and fr[4])

    def wrapper(func):
        argspec = inspect.getargspec(func)
        argnames = list(argspec.args or [])
        defaults = list(argspec.defaults or [])
        defaults = [None] * (len(argnames) - len(defaults)) + defaults
        args = OrderedDict(zip(argnames, defaults))
        if any(args[a] is None for a in args):
            raise TypeError('unbound variables: %s' % (', ').join(a for a in args if args[a] is None))
        checker = Checker(func, args, ntests, nshrinks, nassume, ignore_return=True)

        def wrapped(*args):
            if not (len(args) == 0 or len(args) == 1 and func_is_method):
                raise ValueError('not expecting any arguments')
            result = checker.for_all()
            if result.failed:
                result.reraise()

        wraps(func)(wrapped)
        wrapped.__test__ = True
        return wrapped

    return wrapper