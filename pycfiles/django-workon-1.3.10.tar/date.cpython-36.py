# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/PACKAGES/WORKON/workon/utils/date.py
# Compiled at: 2018-03-30 05:11:29
# Size of source mod 2**32: 13791 bytes
from datetime import datetime, timedelta, date as odate
from collections import namedtuple
import bisect
__all__ = [
 'week_range',
 'first_day_of_quarter',
 'last_day_of_quarter',
 'quarter_range',
 'first_day_of_month',
 'last_day_of_month',
 'month_range',
 'next_month',
 'get_week_number',
 'get_weeks_of_year',
 'Week',
 'DateRange']

def quarter(date):
    return int((date.month - 1) / 3 + 1)


def first_day_of_quarter(date):
    return datetime(date.year, 3 * quarter(date) - 2, 1)


def last_day_of_quarter(date):
    month = 3 * quarter(date)
    remaining = int(month / 12)
    return datetime(date.year + remaining, month % 12 + 1, 1) + timedelta(days=(-1))


def quarter_range(date=None, index=0):
    if not date:
        date = datetime.now().date()
    first_day = first_day_of_quarter(date)
    last_day = last_day_of_quarter(first_day)
    return (first_day, last_day)


def first_day_of_month(date):
    return date.replace(day=1)


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    else:
        return date.replace(month=(date.month + 1), day=1) - timedelta(days=1)


def month_range(date=None, index=0):
    if not date:
        date = datetime.now().date()
    first_day = first_day_of_month(date)
    if index != 0:
        delta = first_day.month + index
        if delta < 1:
            delta = 12
        else:
            if delta > 12:
                delta = 1
        first_day = first_day.replace(month=delta)
    last_day = last_day_of_month(first_day)
    return (first_day, last_day)


def week_range(date=None, index=0):
    one_day = timedelta(days=1)
    week = []
    if not date:
        date = datetime.now().date()
    day_idx = date.weekday() % 7
    sunday = date - timedelta(days=(day_idx - 7 * index))
    date = sunday
    for n in range(7):
        week.append(date)
        date += one_day

    return (
     week[0], week[(-1)])


def next_month(date=None, index=1):
    if not date:
        date = datetime.now().date()
    else:
        year = date.year
        month = date.month + index
        if month > 12:
            month = month - 12
        if month < 1:
            month = 12 + month
            year -= 1
    return date.replace(month=month, day=1, year=year)


class DateRange:

    def __init__(self, start, stop):
        self.start = datetime.combine(start, datetime.min.time())
        self.stop = datetime.combine(stop, datetime.max.time())
        self.year = self.start.year

    def __contains__(self, date):
        return date >= self.start and date <= self.stop

    def __lt__(self, date):
        return date > self.stop

    def __gt__(self, date):
        return date < self.start

    @property
    def range(self):
        return (self.start, self.stop)

    @property
    def is_past(self):
        return datetime.now() > self

    @property
    def is_future(self):
        return datetime.now() < self

    @property
    def is_now(self):
        return datetime.now() in self

    @property
    def days(self):
        return (self.stop - self.start).days + 1

    @property
    def next_year(self):
        return self.move_year(1)

    @property
    def is_week(self):
        return self.start.weekday() == 0 and self.days == 7

    @property
    def week(self):
        return self.week_start

    @property
    def week_start(self):
        return Week(self.start)

    @property
    def week_stop(self):
        return Week(self.stop)

    @property
    def prev_year(self):
        return self.move_year(-1)

    def move_year(self, index):
        return self.__class__(self.start.replace(year=(self.start.year + index)), self.stop.replace(year=(self.stop.year + index)))

    @property
    def next(self):
        days_delta = abs(self.days)
        start = datetime.combine(self.stop + timedelta(days=1), datetime.min.time())
        stop = datetime.combine(start + timedelta(days=days_delta), datetime.max.time())
        return self.__class__(start, stop)

    @property
    def prev(self):
        days_delta = abs(self.days)
        stop = datetime.combine(self.start - timedelta(days=1), datetime.max.time())
        start = datetime.combine(stop - timedelta(days=days_delta), datetime.min.time())
        return self.__class__(start, stop)

    @property
    def weeks(self):
        if self.week_start != self.week_stop:
            return [self.week_start, self.week_stop]
        else:
            return [
             self.week_start]

    def weeks_range_repr(self, prefix='S'):
        return ' - '.join([f"{prefix}{w}" for w in self.weeks])


class Week(DateRange):

    def __init__(self, current=None):
        if not current:
            current = datetime.now().date()
        self.current = current
        self.start = datetime.combine(self.current - timedelta(days=(self.current.weekday())), datetime.min.time())
        self.stop = datetime.combine(self.start + timedelta(days=6), datetime.max.time())
        self.year = self.stop.year if self.number == 1 else self.start.year

    def __str__(self):
        return f"{self.number_zero_filled} ({self.year})"

    def __repr__(self):
        return f"{self.number_zero_filled} ({self.year})"

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop

    @property
    def date_range(self):
        return DateRange(self.start, self.stop)

    @property
    def next_year(self):
        return self.move_year(1)

    @property
    def prev_year(self):
        return self.move_year(-1)

    def move_year(self, index):
        week = self.__class__(self.start.replace(year=(self.year + index)))
        if week.number < self.number:
            week = week.next
        if week.number > self.number:
            week = week.prev
        return week

    @property
    def next(self):
        return self.__class__(self.stop + timedelta(days=1))

    @property
    def prev(self):
        return self.__class__(self.start - timedelta(days=1))

    @property
    def number(self):
        return self.start.isocalendar()[1]

    @property
    def number_zero_filled(self):
        return f"{self.number:02d}"

    @classmethod
    def all_of_year(cls, year=None):
        if not year:
            year = datetime.now().year
        week = cls(odate(year, 1, 1))
        if week.number != 1:
            week = week.next
        while week.year == year:
            yield week
            week = week.next


def get_week_number(date=None, zfill=None, prefix=None):
    if not date:
        date = datetime.now().date()
    number = date.isocalendar()[1]
    return date.isocalendar()[1]


def get_weeks_of_year(year=None):
    weeks = []
    if not year:
        year = datetime.now().year
    start = date(year, 1, 1)
    while start.year == year:
        stop += timedelta(days=(6 - start.weekday()))
        yield (start, stop)
        start += timedelta(days=7)