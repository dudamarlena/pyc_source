# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/logging.py
# Compiled at: 2020-04-19 19:55:58


class FakeLogger(object):

    def debug(self, *args, **kwargs):
        pass

    info = debug
    access = debug
    warn = debug
    error = debug
    simple = debug


logger = FakeLogger()

def default_get_logger(name):
    return logger


class BasicLogger(object):

    def __init__(self, name, subname, func, allowed):
        self.name = name
        self.subname = subname
        self.func = func
        self.allowed = allowed

    def _log(self, log_type, msg, *args, **kwargs):
        if self.allowed and log_type not in self.allowed:
            return
        self.func(('[%s] %s | %s :: %s' % (log_type, self.name,
         self.subname, msg)), *args, **kwargs)

    def simple(self, msg, log_type='log'):
        self._log(log_type, msg)

    def debug(self, *args, **kwargs):
        self._log('debug', (' ').join([ str(a) for a in args ]), **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log('info', msg, *args, **kwargs)

    def access(self, msg, *args, **kwargs):
        self._log('access', msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self._log('warn', msg, *args, **kwargs)

    def error(self, *args, **kwargs):
        self._log('error', (' ').join([ str(a) for a in args ]), **kwargs)


def _log_write(s):
    print s


def get_logger_getter(name, func=_log_write, allowed=[]):
    return lambda subname: BasicLogger(name, subname, func, allowed)