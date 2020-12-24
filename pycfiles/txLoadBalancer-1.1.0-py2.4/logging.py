# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/txlb/logging.py
# Compiled at: 2008-07-05 02:21:36
Logger = None
import sys, time

class _LoggerClass:
    __module__ = __name__

    def __init__(self, logfile=None):
        self.logfile = logfile
        self.fp = None
        self.reopen()
        return

    def reopen(self):
        if self.logfile is not None and self.fp is not None:
            del self.fp
        if self.logfile is None:
            self.fp = sys.stderr
        else:
            self.fp = open(self.logfile, 'a')
        return

    def log(self, message, datestamp=0):
        if datestamp:
            self.fp.write('%s %s' % (self.log_date_time_string(), message))
        else:
            self.fp.write(message)
        self.fp.flush()

    def log_date_time_string(self):
        """Return the current time formatted for logging."""
        now = time.time()
        (year, month, day, hh, mm, ss, x, y, z) = time.localtime(now)
        s = '%02d/%02d/%04d %02d:%02d:%02d' % (day, month, year, hh, mm, ss)
        return s


def initlog(filename):
    global Logger
    Logger = _LoggerClass(filename)


def log(message, datestamp=0):
    global Logger
    if Logger is None:
        Logger = _LoggerClass()
    Logger.log(message, datestamp)
    return


def reload():
    global Logger
    if Logger is None:
        Logger = _LoggerClass()
    Logger.reload()
    return