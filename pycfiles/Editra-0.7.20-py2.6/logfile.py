# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ebmlib/logfile.py
# Compiled at: 2011-02-11 10:39:02
"""
Editra Business Model Library: LogFile

Log file class for managing log files or other transient files that should
be purged after a given period of time.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: logfile.py 66868 2011-02-09 16:01:49Z CJP $'
__revision__ = '$Revision: 66868 $'
__all__ = [
 'LogFile']
import os, time, datetime, re, tempfile

class LogFile(object):
    """Log file class"""

    def __init__(self, prefix, logdir=None):
        """Create a log file
        @param prefix: filename prefix
        @keyword logdir: abs path to log output dir
        @note: if logdir is None then the system temp directory will be used

        """
        super(LogFile, self).__init__()
        self.prefix = prefix
        self.logdir = logdir
        if self.logdir is None:
            self.logdir = tempfile.gettempdir()
        return

    LogDirectory = property(lambda self: self.logdir, lambda self, dname: setattr(self, 'logdir', dname))
    Prefix = property(lambda self: self.prefix, lambda self, prefix: setattr(self, 'prefix', prefix))

    def WriteMessage(self, msg):
        """Append the message to the current log file
        @param msg: string object

        """
        logstamp = '%d_%d_%d' % time.localtime()[:3]
        logname = '%s_%s.log' % (self.prefix, logstamp)
        logpath = os.path.join(self.logdir, logname)
        if os.path.exists(logpath):
            opencmd = 'ab'
        else:
            opencmd = 'wb'
        try:
            handle = open(logpath, opencmd)
            handle.write(msg.rstrip() + os.linesep)
            handle.close()
        except IOError:
            pass

    def PurgeOldLogs(self, days):
        """Purge all log files older than n days
        @param days: number of days

        """
        logpattern = re.compile('%s_[0-9]{4}_[0-9]{1,2}_[0-9]{1,2}.log' % self.prefix)
        paths = list()
        cdate = datetime.date(*time.localtime()[:3])
        for path in os.listdir(self.logdir):
            if logpattern.match(path):
                ymd = [ int(x) for x in path[len(self.prefix) + 1:-4].split('_') ]
                fdate = datetime.date(*ymd)
                span = cdate - fdate
                if span.days > days:
                    fpath = os.path.join(self.logdir, path)
                    paths.append(fpath)

        for log in paths:
            try:
                os.remove(log)
            except OSError:
                pass