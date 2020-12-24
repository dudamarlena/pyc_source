# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/logs/logs.py
# Compiled at: 2020-01-15 07:36:53
# Size of source mod 2**32: 11439 bytes
import re, sys, datetime, argparse
from . import dayutils
from . import daylog

class Logs:
    string_in = 'IN'
    string_out = 'OUT'

    def _get_data_from_files(self):
        data = ''
        for file_log in self._files:
            with open(file_log, 'r') as (f):
                data += f.read()

        return data

    def _get_extreme_days_from_data(self):
        day_id = self._data.split('\n')[0].split()[1]
        start = dayutils.str2day(day_id)
        day_id = self._data.split('\n')[(-2)].split()[1]
        end = dayutils.str2day(day_id)
        return (
         start, end)

    def _get_logs_from_data(self):
        l = []
        for d in dayutils.day_range(self._day_start, self._day_final):
            logs_day = re.findall('.*' + str(d.strftime(dayutils.fmt_id)) + '.*', self._data)
            num_login = len(re.findall(self.string_in, ' '.join(logs_day)))
            num_logout = len(re.findall(self.string_out, ' '.join(logs_day)))
            if num_login and num_login == num_logout:
                logs_day = [i.split()[2] for i in logs_day]
                l.append(daylog.DayLog(d, logs_day))

        l.sort(key=(lambda x: x.uptime()), reverse=True)
        return l

    def __init__(self, list_of_file=[]):
        self._files = list_of_file
        self._data = self._get_data_from_files()
        self._day_start, self._day_final = self._get_extreme_days_from_data()
        self._logs = self._get_logs_from_data()

    def __str__(self):
        return self.report()

    def report(self):

        def _str(k, v):
            return '%s %s\n' % (k.ljust(30, '.'), v)

        s = '\n'
        s += _str('Read data from file', ', '.join(self._files))
        s += _str('First day', self._day_start)
        s += _str('Last day', self._day_final)
        s += _str('Number of days', self.num_days_total())
        s += _str('Number of working days', str(self.num_days_work()) + ' (%.0f%%)' % (100.0 * self.num_days_work() / self.num_days_total()))
        s += _str('Working time total', self.uptime_total())
        d = self.uptime_max()
        s += _str('Working time max', '%s @ %s' % (str(d.uptime()), str(d.date())))
        d = self.uptime_min()
        s += _str('Working time min', '%s @ %s' % (str(d.uptime()), str(d.date())))
        s += _str('Working time average', self.uptime_mean())
        p = self.get_max_uptime_by_day()
        s += _str('Most prolific week day', dayutils.days_long[p[1]] + ' (' + str(p[0]) + ' working time)')
        p = self.get_max_uptime_by_month()
        s += _str('Most prolific month', dayutils.months_long[p[1]] + ' (' + str(p[0]) + ' working time)')
        p = self.get_max_uptime_by_year()
        s += _str('Most prolific year', str(p[1]) + ' (' + str(p[0]) + ' working time)')
        return s

    def num_days_total(self):
        """Return total number of days between start and end days"""
        return (self._day_final - self._day_start).days

    def num_days_work(self):
        """Return number of working days between start and end days"""
        return len(self._logs)

    def days_first(self):
        """Return first day"""
        return self._day_start

    def days_last(self):
        """Return last day"""
        return self._day_final

    def uptime_max(self):
        """Return maximum uptime"""
        return self._logs[0]

    def uptime_min(self):
        """Return minimum uptime"""
        return self._logs[(-1)]

    def uptime_total(self):
        """Return total uptime"""
        up = self.get_from_logs('uptime')
        t = datetime.timedelta(0)
        for i in up:
            t += i

        return t

    def uptime_mean(self):
        """Return mean uptime for day"""
        up = self.uptime_total()
        wd = self.num_days_work()
        return up / wd

    def get_from_logs(self, attribute):
        """Return a list with attribute from daylogs"""
        return [getattr(i, attribute)() for i in self._logs]

    def get_logs(self, condition=lambda x: True):
        """Return logs. If condition is specified return a list of logs satisfying the condition"""
        if condition:
            return [i for i in self._logs if condition(i)]
        else:
            return self._logs

    def sort_logs(self, attribute, reverse=False):
        """Sort logs by attribute"""
        return sorted((self._logs),
          key=(lambda x: getattr(x, attribute)()), reverse=reverse)

    def get_day(self, day):
        """Return a list of daylogs with specified day of month"""
        return self.get_logs(lambda x: x.day().day == day)

    def get_weekday(self, weekday):
        """Return a list of daylogs with specified day of week"""
        return self.get_logs(lambda x: x.day().weekday() == weekday)

    def get_month(self, month):
        """Return a list of daylogs with specified month"""
        return self.get_logs(lambda x: x.day().month == month)

    def get_year(self, year):
        """Return a list of daylogs with specified year"""
        return self.get_logs(lambda x: x.day().year == year)

    def login_early(self):
        """Return earliest login"""
        return self.sort_logs('login')[0]

    def login_last(self):
        """Return latest login"""
        return self.sort_logs('login', True)[0]

    def logout_early(self):
        """Return earliest logout"""
        return self.sort_logs('logout')[0]

    def logout_last(self):
        """Return latest logout"""
        return self.sort_logs('logout', True)[0]

    def daylog_sum(self, l):
        """Return the sum of a list of daylogs"""
        s = daylog.DayLog()
        for i in l:
            s += i

        return s

    def get_logs_by(self, function, ranges):
        """Return a list (with length of ranges) of a list of daylogs that satisfy : function() == index of ranges"""
        return [[j for j in getattr(self, function)(i)] for i in ranges]

    def get_uptime_by_day(self, ranges=list(range(7))):
        """Return a list of list of daylogs accordling to weekday index.
      Default day ranges [0:7].
      0 is Monday
      [ [Mondays], [Tuesdays], ... , [Sundays] ]"""
        l = self.get_logs_by('get_weekday', ranges)
        return [self.daylog_sum(i).uptime() for i in l]

    def get_uptime_by_month(self, ranges=list(range(1, 13))):
        """Return a list of list of daylogs accordling to month index of ranges.
      Default month ranges [1:13].
      1 is January"""
        l = self.get_logs_by('get_month', ranges)
        return [self.daylog_sum(i).uptime() for i in l]

    def get_uptime_by_year(self, ranges=list(range(0, datetime.datetime.today().year))):
        """Return a list of list of daylogs accordling to year index of ranges.
      Default year ranges [0:taday's year]."""
        l = self.get_logs_by('get_year', ranges)
        return [self.daylog_sum(i).uptime() for i in l]

    def get_uptime_by(self, logs_function, search_function):
        """Return uptime and index of uptime accordingly to logs_function and search_function"""
        l = getattr(self, logs_function)()
        uptime = search_function(l)
        index = l.index(uptime)
        return (
         uptime, index)

    def get_max_uptime_by_day(self):
        """Return max uptime and day of max uptime between total uptime of all weekday"""
        return self.get_uptime_by('get_uptime_by_day', max)

    def get_max_uptime_by_month(self):
        """Return max uptime and month of max uptime between total uptime of all month"""
        return self.get_uptime_by('get_uptime_by_month', max)

    def get_max_uptime_by_year(self):
        """Return max uptime and year of max uptime between total uptime of all year"""
        return self.get_uptime_by('get_uptime_by_year', max)


def main():
    parser = argparse.ArgumentParser(prog='',
      formatter_class=(argparse.ArgumentDefaultsHelpFormatter))
    parser.add_argument('--report', action='store_true', help='print report')
    parser.add_argument('--days-tot',
      dest='num_days_total',
      action='store_true',
      help='number of total days')
    parser.add_argument('--days-work',
      dest='num_days_work',
      action='store_true',
      help='number of working days')
    parser.add_argument('--days-first',
      dest='days_first', action='store_true', help='first day')
    parser.add_argument('--days-last',
      dest='days_last', action='store_true', help='last day')
    parser.add_argument('--uptime-tot',
      dest='uptime_total', action='store_true', help='minimum uptime')
    parser.add_argument('--uptime-max', action='store_true', help='maximum uptime')
    parser.add_argument('--uptime-min', action='store_true', help='minimum uptime')
    parser.add_argument('--uptime-mean',
      action='store_true', help='mean uptime for working days')
    parser.add_argument('--login-early', action='store_true', help='earlier login')
    parser.add_argument('--login-last', action='store_true', help='latest login')
    parser.add_argument('--logout-early', action='store_true', help='earlier logout')
    parser.add_argument('--logout-last', action='store_true', help='latest logout')
    parser.add_argument('files', nargs='+', help='File [File ... ]')
    args = parser.parse_args()
    a = Logs(args.files)
    for k, v in sorted(vars(args).items()):
        if v and isinstance(v, bool):
            d = getattr(a, k)()
            if d:
                print('%s : %s' % (re.sub('_', ' ', k).ljust(15), d))

    print(a.report())


if __name__ == '__main__':
    main()