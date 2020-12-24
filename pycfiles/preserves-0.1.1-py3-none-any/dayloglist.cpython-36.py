# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/logs/dayloglist.py
# Compiled at: 2020-01-15 07:36:53
# Size of source mod 2**32: 1047 bytes
import datetime
from . import dayutils
from .daylog import DayLog

class DayLogList(list):

    def __init__(self):
        self.daylog = DayLog()

    def __str__(self):
        s = '[LIST] '
        s += '{:.<20}'.format('Date')
        s += '{}\n'.format(', '.join([i.date(True) for i in self]))
        s += '       ' + '{:.<20}'.format('Up')
        s += '{}\n'.format(', '.join([dayutils.sec2str(i.uptime().total_seconds()) for i in self]))
        s += '       ' + '{:.<20}'.format('Logs')
        for j in self:
            s += '[{}] '.format(', '.join([i.time().strftime(dayutils.fmt_time) for i in j.logs()]))

        s += '\n'
        s += '       ' + '{:.<20}{}\n'.format('Uptime', dayutils.sec2str(self.daylog.uptime().total_seconds()))
        return s

    def append(self, args):
        list.append(self, args)
        self.daylog['uptime'] += args['uptime']