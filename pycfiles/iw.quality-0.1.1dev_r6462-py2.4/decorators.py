# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/quality/decorators.py
# Compiled at: 2007-10-18 16:14:48
""" Decorators
"""
import logging, time, datetime

def _formatter(total, function, args, kw):
    """default rendering"""

    def _fmt(element):
        if hasattr(element, 'func_name'):
            return element.func_name
        return element

    func_name = _fmt(function)
    args = tuple([ _fmt(arg) for arg in args ])
    now = datetime.datetime.now().isoformat()
    msg = "function '%s', args: %s, kw: %s" % (func_name, str(args), str(kw))
    return 'log_time::%s::%.3f::%s' % (now, total, msg)


def log_time(treshold=0, logger=logging.info, formatter=_formatter, debugger=None):
    """ timedtest decorator
    decorates the test method with a timer
    when the time spent by the test exceeds
    max_time in seconds, an Assertion error is thrown.
    """

    def _timedtest(function):

        def wrapper(*args, **kw):
            start = time.time()
            try:
                try:
                    return function(*args, **kw)
                except Exception, e:
                    if debugger is not None:
                        debugger(e)
                    raise e

            finally:
                total = time.time() - start
                if total > treshold:
                    logger(formatter(total, function, args, kw))
            return

        return wrapper

    return _timedtest