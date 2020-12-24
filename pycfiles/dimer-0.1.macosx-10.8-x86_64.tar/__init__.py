# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/__init__.py
# Compiled at: 2013-07-11 19:10:33
"""root package"""
import logging, time, warnings
log = logging.getLogger(__name__)

def measure_time(funct):
    """decorator that measures the time spent in a function"""

    def newf(*args, **kwargs):
        """with time"""
        start_time = time.time()
        res = funct(*args, **kwargs)
        log.info('operation took %.2f seconds\n', time.time() - start_time)
        return res

    return newf


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    def newfunc(*args, **kwargs):
        warnings.warn('Call to deprecated function %s.' % func.__name__, category=DeprecationWarning)
        return func(*args, **kwargs)

    newfunc.__name__ = func.__name__
    newfunc.__doc__ = func.__doc__
    newfunc.__dict__.update(func.__dict__)
    return newfunc