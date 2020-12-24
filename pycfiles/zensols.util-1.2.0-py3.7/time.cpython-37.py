# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/util/time.py
# Compiled at: 2020-04-25 21:22:01
# Size of source mod 2**32: 4802 bytes
"""Peformance measure convenience utils.

"""
__author__ = 'Paul Landes'
import logging, inspect, time as tm
from functools import wraps
import errno, os, signal
time_logger = logging.getLogger(__name__)

class time(object):
    __doc__ = "Used in a ``with`` scope that executes the body and logs the elapsed time.\n\n    Format f-strings are supported as the locals are taken from the calling\n    frame on exit.  This means you can do things like:\n\n        with time('processed {cnt} items'):\n            cnt = 5\n            tm.sleep(1)\n\n    which produeces: ``processed 5 items``.\n\n    See the initializer documentation about special treatment for global\n    loggers.\n\n    "

    def __init__(self, msg, level=logging.INFO, logger=None):
        """Create the time object.

        If a logger is not given, it is taken from the calling frame's global
        variable named ``logger``.  If this global doesn't exit it logs to
        standard out.

        You can force standard out instead of a logger by using 

        :param msg: the message log when exiting the closure
        :param logger: the logger to use for logging or the string ``stdout``
                       for printing to standard
        :param level: the level at which the message is logged

        """
        self.msg = msg
        self.logger = logger
        self.level = level
        frame = inspect.currentframe()
        try:
            globs = frame.f_back.f_globals
            if 'logger' in globs:
                self.logger = globs['logger']
        except Exception as e:
            try:
                time_logger.error(e)
            finally:
                e = None
                del e

    def __enter__(self):
        self.t0 = tm.time()

    def __exit__(self, type, value, traceback):
        elapse = tm.time() - self.t0
        msg = self.msg
        frame = inspect.currentframe()
        try:
            locals = frame.f_back.f_locals
            msg = (msg.format)(**locals)
        except Exception as e:
            try:
                time_logger.error(e)
            finally:
                e = None
                del e

        msgstr = f"{msg} in {elapse:.1f}s"
        if self.logger is not None:
            self.logger.log(self.level, msgstr)
        else:
            print(msgstr)


class TimeoutError(Exception):
    pass


TIMEOUT_DEFAULT = 10

def timeout(seconds=TIMEOUT_DEFAULT, error_message=os.strerror(errno.ETIME)):
    """This creates a decorator called @timeout that can be applied to any long
    running functions.

    So, in your application code, you can use the decorator like so:

        from timeout import timeout

        # Timeout a long running function with the default expiry of
        # TIMEOUT_DEFAULT seconds.
        @timeout
        def long_running_function1():

    :see https://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish:
    :author David Narayan

    """

    def decorator(func):

        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)

            return result

        return wraps(func)(wrapper)

    return decorator


class timeprotect(object):
    __doc__ = 'Invokes a block and bails if not completed in a specified number of seconds.\n\n    :param seconds: the number of seconds to wait\n\n    :param timeout_handler: function that takes a single argument, which is\n                            this ``timeprotect`` object instance; if ``None``,\n                            then nothing is done if the block times out\n\n    :param context: an object accessible from the ``timeout_hander`` via\n                          ``self``, which defaults to ``None``\n\n    :see timeout:\n\n    '

    def __init__(self, seconds=TIMEOUT_DEFAULT, timeout_handler=None, context=None, error_message=os.strerror(errno.ETIME)):
        self.seconds = seconds
        self.timeout_handler = timeout_handler
        self.context = context
        self.error_message = error_message
        self.timeout_handler_exception = None

    def __enter__(self):

        def _handle_timeout(signum, frame):
            signal.alarm(0)
            if self.timeout_handler is not None:
                try:
                    self.timeout_handler(self)
                except Exception as e:
                    try:
                        time_logger.exception(f"could not recover from timeout handler: {e}")
                        self.timeout_handler_exception = e
                    finally:
                        e = None
                        del e

            raise TimeoutError(self.error_message)

        signal.signal(signal.SIGALRM, _handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, cls, value, traceback):
        signal.alarm(0)
        return True