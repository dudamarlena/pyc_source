# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/redislog/logger.py
# Compiled at: 2011-06-02 01:56:05
import socket, getpass, datetime, inspect, logging

def levelAsString(level):
    return {logging.DEBUG: 'debug', logging.INFO: 'info', 
       logging.WARNING: 'warning', 
       logging.ERROR: 'error', 
       logging.CRITICAL: 'critical', 
       logging.FATAL: 'fatal'}.get(level, 'unknown')


def _getCallingContext():
    """
    Utility function for the RedisLogRecord.

    Returns the module, function, and lineno of the function 
    that called the logger.  
 
    We look way up in the stack.  The stack at this point is:
    [0] logger.py _getCallingContext (hey, that's me!)
    [1] logger.py __init__
    [2] logger.py makeRecord
    [3] _log
    [4] <logging method>
    [5] caller of logging method
    """
    frames = inspect.stack()
    if len(frames) > 4:
        context = frames[5]
    else:
        context = frames[0]
    modname = context[1]
    lineno = context[2]
    if context[3]:
        funcname = context[3]
    else:
        funcname = ''
    del context
    del frames
    return (
     modname, funcname, lineno)


class RedisLogRecord(logging.LogRecord):

    def __init__(self, name, lvl, fn, lno, msg, args, exc_info, func=None, extra=None):
        logging.LogRecord.__init__(self, name, lvl, fn, lno, msg, args, exc_info, func)
        self.hostname = socket.gethostname()
        self.username = getpass.getuser()
        (self.modname, self.funcname, self.lineno) = _getCallingContext()
        self._raw = {'name': name, 
           'level': levelAsString(lvl), 
           'filename': fn, 
           'line_no': self.lineno, 
           'msg': str(msg), 
           'args': list(args), 
           'time': datetime.datetime.utcnow(), 
           'username': self.username, 
           'funcname': self.funcname, 
           'hostname': self.hostname, 
           'traceback': exc_info}


class RedisLogger(logging.getLoggerClass()):

    def makeRecord(self, name, lvl, fn, lno, msg, args, exc_info, func=None, extra=None):
        record = RedisLogRecord(name, lvl, fn, lno, msg, args, exc_info, func=None)
        if extra:
            for key in extra:
                if key in ('message', 'asctime') or key in record.__dict__:
                    raise KeyError('Attempt to overwrite %r in RedisLogRecord' % key)
                record.__dict__[key] = extra[key]

        return record