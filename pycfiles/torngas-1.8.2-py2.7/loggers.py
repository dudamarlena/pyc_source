# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/torngas/logger/loggers.py
# Compiled at: 2016-02-16 00:41:00
import os, time
from glob import glob
import logging, logging.handlers

class ProcessLogTimedFileHandler(logging.handlers.TimedRotatingFileHandler):

    def __init__(self, filename, when='h', interval=1, backupCount=20, encoding=None, delay=False, utc=False):
        self.delay = delay
        super(ProcessLogTimedFileHandler, self).__init__(filename, when, interval, backupCount, encoding, delay, utc)

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[(-1)]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[(-1)]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
            dfn = self.baseFilename + '.' + time.strftime(self.suffix, timeTuple)
            if os.path.exists(dfn):
                os.remove(dfn)
            try:
                if not glob(dfn + '.*') and os.path.exists(self.baseFilename):
                    os.rename(self.baseFilename, dfn + '.%d' % os.getpid())
            except OSError:
                pass

            if self.backupCount > 0:
                for s in self.getFilesToDelete():
                    os.remove(s)

            if not self.delay:
                self.stream = self._open()
            newRolloverAt = self.computeRollover(currentTime)
            while newRolloverAt <= currentTime:
                newRolloverAt = newRolloverAt + self.interval

        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[(-1)]
            if dstNow != dstAtRollover:
                if not dstNow:
                    addend = -3600
                else:
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
        return