# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmpy_util/schedule_util.py
# Compiled at: 2020-01-09 23:05:29
# Size of source mod 2**32: 12116 bytes
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : schedule_util.py
@Desc    : 定时任务
"""
import schedule, logging, threading, time
from datetime import datetime
from functools import wraps
import calendar, re
logger = logging.getLogger(__name__)

class ScheduleManger:

    def __init__(self, interval=1):
        self._quaz_flag = True
        self._interval = interval
        self._thread = None

    def do_work(self):
        while self._quaz_flag:
            time.sleep(self._interval)
            schedule.run_pending()

    def start_time(self):
        if self._thread is None:
            self._thread = threading.Thread(target=(self.do_work))
            self._thread.daemon = True
        if not self._thread.is_alive():
            self._thread.start()

    def stop_timer(self):
        self._quaz_flag = False

    def add_schedule(self, every, job, args=(), kwargs={}):
        """
        增加定时任务
        :param every: 时间间隔：秒
        :param job:
        :param args:
        :param kwargs:
        :return:
        """
        if args is None:
            args = tuple()
        else:
            if kwargs is None:
                kwargs = dict()
            if not isinstance(args, list):
                if not isinstance(args, tuple):
                    args = (
                     args,)
        (schedule.every(every).seconds.do)(job, *args, **kwargs)

    def add_schedule_at_time(self, time_str, job, args=(), kwargs={}):
        (schedule.every().days.at(time_str).do)(job, *args, **kwargs)


schedule_manager = ScheduleManger()
month_mappings = {'JAN':1, 
 'FEB':2,  'MAR':3,  'APR':4,  'MAY':5,  'JUN':6,  'JUL':7,  'AUG':8,  'SEP':9,  'OCT':10,  'NOW':11, 
 'DEC':12}
re_year = '(?P<years>(19[789]\\d{1}|[2-9]\\d{3}|\\*)(/[1-9]\\d*)?|(19[789]\\d{1}|[2-9]\\d{3})-(19[789]\\d{1}|[2-9]\\d{3})|(19[789]\\d{1}|[2-9]\\d{3})(-(19[789]\\d{1}|[2-9]\\d{3}))?(,(19[789]\\d{1}|[2-9]\\d{3})(-(19[789]\\d{1}|[2-9]\\d{3}))?)+)'
re_month = '(?P<months>((0?[1-9]|1[012])|\\*)(/[1-9]\\d*)?|(0?[1-9]|1[012])-(0?[1-9]|1[012])|(0?[1-9]|1[012])(-(0?[1-9]|1[012]))?(,(0?[1-9]|1[012])(-(0?[1-9]|1[012]))?)+|(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)|(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)|(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)(-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC))?(,(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC)(-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOW|DEC))?)+)'
re_day = '(?P<days>((0?[1-9]|[12]\\d|3[01])|\\*)(/[1-9]\\d*)?|(0?[1-9]|[12]\\d|3[01])-(0?[1-9]|[12]\\d|3[01])|(0?[1-9]|[12]\\d|3[01])(-(0?[1-9]|[12]\\d|3[01]))?(,(0?[1-9]|[12]\\d|3[01])(-(0?[1-9]|[12]\\d|3[01]))?)+)'
re_hour = '(?P<hours>(([01]?\\d|2[0123])|\\*)(/[1-9]\\d*)?|([01]?\\d|2[0123])-([01]?\\d|2[0123])|([01]?\\d|2[0123])(-([01]?\\d|2[0123]))?(,([01]?\\d|2[0123])(-([01]?\\d|2[0123]))?)+)'
re_minute = '(?P<minutes>([0-5]?\\d|\\*)(/[1-9]\\d*)?|[0-5]?\\d-[0-5]?\\d|[0-5]?\\d(-[0-5]?\\d)?(,[0-5]?\\d(-[0-5]?\\d)?)+)'
re_second = '(?P<seconds>([0-5]?\\d|\\*)(/[1-9]\\d*)?|[0-5]?\\d-[0-5]?\\d|[0-5]?\\d(-[0-5]?\\d)?(,[0-5]?\\d(-[0-5]?\\d)?)+)'
cron_expression = '^%s\\s+%s\\s+%s\\s+%s\\s+%s\\s+%s$' % (re_year, re_month, re_day, re_hour, re_minute, re_second)
re_range = '.*[-,].*'
re_star = '\\*'
re_forward_flash = '/'
min_year, min_month, min_day, min_hour, min_minute, min_second = (1970, 1, 1, 0, 0,
                                                                  0)
max_year, max_month, max_day, max_hour, max_minute, max_second = (10000, 13, 32, 24,
                                                                  60, 60)

class CronError(Exception):

    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return repr(self.error_msg)


class Cron:

    def __init__(self, cron, init_datetime=datetime.now()):
        self._Cron__init_year = init_datetime.year
        self._Cron__init_month = init_datetime.month
        self._Cron__init_day = init_datetime.day
        self._Cron__init_hour = init_datetime.hour
        self._Cron__init_minute = init_datetime.minute
        self._Cron__init_second = init_datetime.second
        match = re.match(cron_expression, cron)
        if match is not None:
            years = match.group('years')
            self._Cron__years = self._Cron__resolve(years, min_year, max_year)
            months = match.group('months')
            for key, value in month_mappings.items():
                months = months.replace(key, str(value))

            self._Cron__months = self._Cron__resolve(months, min_month, max_month)
            days = match.group('days')
            self._Cron__days = self._Cron__resolve(days, min_day, max_day)
            hours = match.group('hours')
            self._Cron__hours = self._Cron__resolve(hours, min_hour, max_hour)
            minutes = match.group('minutes')
            self._Cron__minutes = self._Cron__resolve(minutes, min_minute, max_minute)
            seconds = match.group('seconds')
            self._Cron__seconds = self._Cron__resolve(seconds, min_second, max_second)
        else:
            raise CronError('Cron Expression Format Error')

    def __resolve(self, field_value, min_value, max_value):
        if re.match(re_range, field_value):
            points = self._Cron__flatten(field_value)
        else:
            values = re.split(re_forward_flash, field_value)
            if re.match(re_star, field_value):
                period = 1 if len(values) == 1 else int(values[1])
                points = [i for i in range(min_value, max_value, period)]
            else:
                period = None if len(values) == 1 else int(values[1])
                if period is None:
                    points = [
                     int(values[0])]
                else:
                    points = [i for i in range(int(values[0]), max_value, period)]
        return points

    def __flatten(self, ranges=''):
        values = []
        for r in [re.split('-', i) for i in re.split(',', ranges)]:
            if len(r) == 2:
                values += [i for i in range(int(r[0]), int(r[1]) + 1)]
            else:
                if len(r) == 1:
                    values.append(int(r[0]))

        return sorted(set(values))

    def next_execute_time(self):
        for year in self._Cron__years:
            if year < self._Cron__init_year:
                pass
            else:
                for month in self._Cron__months:
                    if year <= self._Cron__init_year:
                        if month < self._Cron__init_month:
                            continue
                    current_max_day = calendar.monthrange(year, month)[1] + 1
                    days = [i for i in filter(lambda x: x < current_max_day, self._Cron__days)]
                    for day in days:
                        if year <= self._Cron__init_year:
                            if month <= self._Cron__init_month:
                                if day < self._Cron__init_day:
                                    continue
                        for hour in self._Cron__hours:
                            if year <= self._Cron__init_year:
                                if month <= self._Cron__init_month:
                                    if day <= self._Cron__init_day:
                                        if hour < self._Cron__init_hour:
                                            continue
                            for minute in self._Cron__minutes:
                                if year <= self._Cron__init_year:
                                    if month <= self._Cron__init_month:
                                        if day <= self._Cron__init_day:
                                            if hour <= self._Cron__init_hour:
                                                if minute < self._Cron__init_minute:
                                                    continue
                                for second in self._Cron__seconds:
                                    if year <= self._Cron__init_year:
                                        if month <= self._Cron__init_month:
                                            if day <= self._Cron__init_day:
                                                if hour <= self._Cron__init_hour:
                                                    if minute <= self._Cron__init_minute:
                                                        if second < self._Cron__init_second:
                                                            continue
                                    yield datetime(year, month, day, hour, minute, second)


def scheduler(cron, retry_times=3, retry_interval=5, excludes=(), includes=()):
    """
    调用样例
    @scheduler("* * * * 0/5 0")
    def func():
        ...
    每隔5分钟调用一次指定函数

    :param cron:
    :param retry_times:
    :param retry_interval:
    :param excludes:
    :param includes:
    :return:
    """
    scheduler_cron = Cron(cron)
    execute_datetime = scheduler_cron.next_execute_time()

    def decorator(func):

        @wraps(func)
        def wrapper():
            try:
                next_interval = (next(execute_datetime) - datetime.now()).total_seconds()
                threading.Timer(interval=next_interval, function=wrapper).start()
            except StopIteration:
                logger.warning('there is no next-execution-datetime found')

            executed_times = 0
            while executed_times <= retry_times:
                try:
                    logger.debug('start to execute the task %s', func.__name__)
                    func()
                    logger.debug('finish to execute the task %s', func.__name__)
                except Exception as e:
                    logger.error('it is failure to execute the task %s, the error is %s', func.__name__, str(e))
                    is_exclude = False
                    for exclude in excludes:
                        if isinstance(e, exclude):
                            is_exclude = True

                    if is_exclude:
                        raise e
                    is_include = False
                    for include in includes:
                        if isinstance(e, include):
                            is_include = True

                    if is_include or len(includes) == 0:
                        if executed_times < retry_times:
                            time.sleep(retry_interval)
                        executed_times += 1
                    else:
                        raise e
                    if executed_times > retry_times:
                        raise e
                else:
                    break

        try:
            next_execution_datetime = next(execute_datetime)
            while not (next_execution_datetime - datetime.now()).total_seconds() > 0:
                next_execution_datetime = next(execute_datetime)

            interval = (next_execution_datetime - datetime.now()).total_seconds()
            threading.Timer(interval=interval, function=wrapper).start()
            return wrapper
        except StopIteration:
            logger.warning('there is no next-execution-datetime found')

    return decorator


def add_scheduler_task(func, cron, retry_times=3, retry_interval=5, excludes=(), includes=()):
    scheduler(cron, retry_times, retry_interval, excludes, includes)(func)


if __name__ == '__main__':

    def my_job(name, *args, **kwargs):
        print(args, kwargs)
        print('my name is %s, at %.2f' % (name, time.time()))


    s = ScheduleManger()
    s.add_schedule(6, my_job, ('zww', 'haha', 123), dict(a=1, b=2))
    s.add_schedule(3, my_job, ('ly', 'lala', '456'), dict(jaja=1))
    time.sleep(10)
    s.add_schedule(1, my_job, ('yx', 'jiji', 222), dict(bibi=2))
    a = input()
    s.stop_timer()
    time.sleep(100)