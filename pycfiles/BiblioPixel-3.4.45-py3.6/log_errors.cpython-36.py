# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/log_errors.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1450 bytes
from ..util import class_name, log

class LogErrors:
    __doc__ = '\n    Wraps a function call to catch and report exceptions.\n    '

    def __init__(self, function, errors):
        """
        :param function: the function to wrap
        :param errors: either a number, indicating how many errors to report
           before ignoring them, or one of these strings:
           'raise', meaning to raise an exception
           'ignore', meaning to ignore all errors
           'report', meaning to report all errors
        """
        if not isinstance(errors, int):
            if not errors in ('raise', 'ignore', 'report'):
                raise AssertionError
        self.function = function
        self.errors = errors
        self.error_count = 0

    def __call__(self, *args, **kwds):
        """
        Calls `self.function` with the given arguments and keywords, and
        returns its value - or if the call throws an exception, returns None.
        """
        try:
            return (self.function)(*args, **kwds)
        except Exception as e:
            self.error_count += 1
            if self.errors == 'raise':
                raise
            if self.errors == 'ignore':
                return
            args = (
             class_name.class_name(e),) + e.args

        if self.errors == 'report' or self.error_count <= self.errors:
            log.error(str(args))
        elif self.error_count == self.errors + 1:
            log.error('Exceeded errors of %d', self.errors)