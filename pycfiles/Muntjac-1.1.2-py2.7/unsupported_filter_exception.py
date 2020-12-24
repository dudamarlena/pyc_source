# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/util/filter/unsupported_filter_exception.py
# Compiled at: 2013-04-04 15:36:37
"""Exception for cases where a container does not support a specific
type of filters."""

class UnsupportedFilterException(RuntimeError):
    """Exception for cases where a container does not support a specific
    type of filters.

    If possible, this should be thrown already when adding a filter to a
    container. If a problem is not detected at that point, an
    L{NotImplementedError} can be thrown when attempting to perform filtering.
    """

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 0:
            pass
        elif nargs == 1:
            if isinstance(args[0], Exception):
                cause, = args
                super(UnsupportedFilterException, self).__init__(cause)
            else:
                message, = args
                super(UnsupportedFilterException, self).__init__(message)
        elif nargs == 2:
            message, cause = args
            super(UnsupportedFilterException, self).__init__(message, cause)
        else:
            raise ValueError