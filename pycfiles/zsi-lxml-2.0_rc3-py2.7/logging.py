# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZSI/wstools/logging.py
# Compiled at: 2006-10-25 20:34:29
"""Logging"""
ident = '$Id: logging.py 1204 2006-05-03 00:13:47Z boverhof $'
import sys
WARN = 1
DEBUG = 2

class ILogger:
    """Logger interface, by default this class
    will be used and logging calls are no-ops.
    """
    level = 0

    def __init__(self, msg):
        pass

    def warning(self, *args):
        pass

    def debug(self, *args):
        pass

    def error(self, *args):
        pass

    def setLevel(cls, level):
        cls.level = level

    setLevel = classmethod(setLevel)
    debugOn = lambda self: self.level >= DEBUG
    warnOn = lambda self: self.level >= WARN


class BasicLogger(ILogger):
    last = ''

    def __init__(self, msg, out=sys.stdout):
        self.msg, self.out = msg, out

    def warning(self, msg, *args):
        if self.warnOn() is False:
            return
        if BasicLogger.last != self.msg:
            BasicLogger.last = self.msg
            print >> self, '---- ', self.msg, ' ----'
        print >> self, '    %s  ' % BasicLogger.WARN,
        print >> self, msg % args

    WARN = '[WARN]'

    def debug(self, msg, *args):
        if self.debugOn() is False:
            return
        if BasicLogger.last != self.msg:
            BasicLogger.last = self.msg
            print >> self, '---- ', self.msg, ' ----'
        print >> self, '    %s  ' % BasicLogger.DEBUG,
        print >> self, msg % args

    DEBUG = '[DEBUG]'

    def error(self, msg, *args):
        if BasicLogger.last != self.msg:
            BasicLogger.last = self.msg
            print >> self, '---- ', self.msg, ' ----'
        print >> self, '    %s  ' % BasicLogger.ERROR,
        print >> self, msg % args

    ERROR = '[ERROR]'

    def write(self, *args):
        """Write convenience function; writes strings.
        """
        for s in args:
            self.out.write(s)


_LoggerClass = BasicLogger

def setBasicLogger():
    """Use Basic Logger. 
    """
    setLoggerClass(BasicLogger)
    BasicLogger.setLevel(0)


def setBasicLoggerWARN():
    """Use Basic Logger.
    """
    setLoggerClass(BasicLogger)
    BasicLogger.setLevel(WARN)


def setBasicLoggerDEBUG():
    """Use Basic Logger.
    """
    setLoggerClass(BasicLogger)
    BasicLogger.setLevel(DEBUG)


def setLoggerClass(loggingClass):
    """Set Logging Class.
    """
    global _LoggerClass
    assert issubclass(loggingClass, ILogger), 'loggingClass must subclass ILogger'
    _LoggerClass = loggingClass


def setLevel(level=0):
    """Set Global Logging Level.
    """
    ILogger.level = level


def getLevel():
    return ILogger.level


def getLogger(msg):
    """Return instance of Logging class.
    """
    return _LoggerClass(msg)