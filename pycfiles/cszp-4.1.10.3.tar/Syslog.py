# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/Syslog.py
# Compiled at: 2009-11-25 02:40:11
__doc__ = "Celestial Software's Syslog utilities\n\nThe Csys.Syslog class separates out the syslog time, program,\nprocess id and the remainder of the command for ease of use\nin log processing programs.\n\n$Id: Syslog.py,v 1.3 2009/11/25 07:40:11 csoftmgr Exp $"
__version__ = '$Revision: 1.3 $'[11:-2]
import re, sys, time, datetime, Csys
from Csys.Dates import getdate
_curtime = long(time.time())
_today = datetime.date.today()
_year = int(str(_today)[:4])

class Syslog(Csys.CSClass):
    _attributes = dict(time=0, host='', program=None, entry='', pid=0, type=None, utime=0)
    _pattern_1 = re.compile('^(.{15})\\s+(\\S+)\\s+([^:]*):\\s+(.*)')
    _pattern_1a = re.compile('^(.{15})\\s+(\\S+)\\s+(.*)')
    _pattern_2 = re.compile('^<([^>]*)>\\s+(.*)')
    _pattern_3 = re.compile('^(.*)\\[(\\d*)\\]')
    _last_utime = 0

    def __init__(self, inputline, pattern=None):
        global _year
        Csys.CSClass.__init__(self)
        r = Syslog._pattern_1.search(inputline)
        if r:
            self.time = r.group(1)
            self.host = r.group(2)
            self.program = r.group(3)
            self.entry = r.group(4)
        else:
            r = Syslog._pattern_1a.search(inputline)
            self.time = r.group(1)
            self.host = r.group(2)
            self.program = None
            self.entry = r.group(3)
        while True:
            strdate = '%s %d' % (self.time, _year)
            self.utime = getdate(strdate)
            if self.utime < Syslog._last_utime:
                _year += 1
                continue
            if self.utime <= long(time.time()):
                break
            _year -= 1

        Syslog._last_utime = self.utime
        if self.program:
            r = Syslog._pattern_2.search(self.program)
            if r:
                self.type = r.group(1)
                self.program = r.group(2)
            if pattern:
                self.program = re.sub(pattern, '', self.program)
            r = Syslog._pattern_3.search(self.program)
            if r:
                self.program = r.group(1)
                self.pid = int(r.group(2))
        return


if __name__ == '__main__':
    print 'OK'
    print _curtime
    print _today
    print _year
    try:
        fh = open('/tmp/syslog')
    except:
        sys.exit(0)

    for line in fh:
        line = line.rstrip()
        print line
        sl = Syslog(line)
        print '%s[%d]' % (sl.program, sl.pid)