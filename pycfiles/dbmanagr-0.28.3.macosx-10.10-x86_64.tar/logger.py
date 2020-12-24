# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/logger.py
# Compiled at: 2015-10-11 07:17:06
import sys, logging, time, functools, inspect
logger = logging.getLogger(__name__)
ENTRY_MESSAGE = '⇢ %s({})'
EXIT_MESSAGE = '⇠ %s [%0.3fms] = %s'

def encode(v):
    if v is None:
        return
    else:
        if type(v) is unicode:
            return repr(v)
        if type(v) is str:
            return encode(unicode(v, 'UTF-8'))
        if type(v) is list:
            return map(encode, v)
        return encode(unicode(v))


def argtostring(k, v):
    if k == 'self':
        return k
    return ('{0}={1}').format(k, encode(v))


def log_error(e):
    sys.stderr.write(('{0}: {1}\n').format(sys.argv[0].split('/')[(-1)], e))


class LogWith(object):
    """Logging decorator that allows you to log with a specific logger.
"""

    def __init__(self, logger, log_args=True, log_result=True):
        self.logger = logger
        self.log_args = log_args
        self.log_result = log_result

    def __call__(self, f):
        """Returns a wrapper that wraps function f. The wrapper will log the
entry and exit points of the function with logging.DEBUG level.
"""

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if self.logger.getEffectiveLevel() <= logging.DEBUG:
                if self.log_args:
                    cargs = inspect.getcallargs(f, *args)
                    fargs = map(lambda k: argtostring(k, cargs[k]), inspect.getargspec(f).args)
                    fargs += map(lambda (k, v): encode(v), kwargs)
                    formats = map(lambda arg: '%s', fargs)
                    formats += map(lambda (k, v): ('{}=%s').format(k), kwargs)
                    self.logger.debug(ENTRY_MESSAGE.format((', ').join(formats)), f.__name__, *fargs)
                else:
                    self.logger.debug(ENTRY_MESSAGE.format('<omitted>'), f.__name__)
                start = time.time()
                result = f(*args, **kwargs)
                if self.log_result:
                    self.logger.debug(EXIT_MESSAGE, f.__name__, (time.time() - start) * 1000.0, encode(result))
                else:
                    self.logger.debug(EXIT_MESSAGE, f.__name__, (time.time() - start) * 1000.0, '<omitted>')
                return result
            return f(*args, **kwargs)

        return wrapper


class LogTimer(object):

    def __init__(self, logger, subject, prolog=None, *pargs):
        self.logger = logger
        self.subject = subject
        self.start = time.time()
        if prolog is not None:
            self.logger.info(prolog, *pargs)
        return

    def stop(self):
        self.logger.info('%s took: %0.6fs', self.subject, time.time() - self.start)