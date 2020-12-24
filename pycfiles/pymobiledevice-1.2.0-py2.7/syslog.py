# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/syslog.py
# Compiled at: 2019-03-03 17:03:26
import re, logging
from pymobiledevice.lockdown import LockdownClient
from six import PY3
from sys import exit
from datetime import datetime
from util import getHomePath
from util import hexdump
from sys import exit
from optparse import OptionParser
import time
TIME_FORMAT = '%H:%M:%S'

class Syslog(object):
    """
    View system logs
    """

    def __init__(self, lockdown=None, udid=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.lockdown = lockdown if lockdown else LockdownClient(udid=udid)
        self.c = self.lockdown.startService('com.apple.syslog_relay')
        if self.c:
            self.c.send('watch')
        else:
            exit(1)

    def watch(self, watchtime=None, logFile=None, procName=None):
        """View log
        :param watchtime: time (seconds)
        :type watchtime: int
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0:param logFile: full path to the log file
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0:type logFile: str
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0:param procName: process name
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0:type proName: str
        """
        begin = time.strftime(TIME_FORMAT)
        while True:
            d = self.c.recv(4096)
            if PY3:
                d = d.decode('utf-8')
            if procName:
                procFilter = re.compile(procName, re.IGNORECASE)
                if len(d.split(' ')) > 4 and not procFilter.search(d):
                    continue
            s = d.strip('\n\x00\x00')
            print s
            if logFile:
                with open(logFile, 'a') as (f):
                    f.write(d.replace('\x00', ''))
            if watchtime:
                now = self.time_match(s[7:15])
                if now:
                    time_spend = self.time_caculate(str(begin), now)
                    if time_spend > watchtime:
                        break

    def time_match(self, str_time):
        """
        Determine if the time format matches
        """
        pattern = re.compile('\\d{2}:\\d{2}:\\d{2}')
        match = pattern.match(str_time)
        if match:
            return str_time
        else:
            return False

    def time_caculate(self, a, b):
        """
        Calculate the time difference between two strings
        """
        time_a = int(a[6:8]) + 60 * int(a[3:5]) + 3600 * int(a[0:2])
        time_b = int(b[6:8]) + 60 * int(b[3:5]) + 3600 * int(b[0:2])
        time_a = int(a[6:8]) + 60 * int(a[3:5]) + 3600 * int(a[0:2])
        time_b = int(b[6:8]) + 60 * int(b[3:5]) + 3600 * int(b[0:2])
        return time_b - time_a


if __name__ == '__main__':
    parser = OptionParser(usage='%prog')
    parser.add_option('-u', '--udid', default=False, action='store', dest='device_udid', metavar='DEVICE_UDID', help='Device udid')
    parser.add_option('-p', '--process', dest='procName', default=False, help='Show process log only', type='string')
    parser.add_option('-o', '--logfile', dest='logFile', default=False, help='Write Logs into specified file', type='string')
    parser.add_option('-w', '--watch-time', default=False, action='store', dest='watchtime', metavar='WATCH_TIME', help='watchtime')
    options, args = parser.parse_args()
    try:
        try:
            logging.basicConfig(level=logging.INFO)
            lckdn = LockdownClient(options.device_udid)
            syslog = Syslog(lockdown=lckdn)
            syslog.watch(watchtime=int(options.watchtime), procName=options.procName, logFile=options.logFile)
        except KeyboardInterrupt:
            print 'KeyboardInterrupt caught'
            raise

    except (KeyboardInterrupt, SystemExit):
        exit()