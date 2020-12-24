# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/dates.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = ' Defines date methods and helpers for manipulating date information. '
import datetime
from projex.enum import enum
RepeatFlags = enum('EveryMonday', 'EveryTuesday', 'EveryWednesday', 'EveryThursday', 'EveryFriday', 'EverySaturday', 'EverySunday', 'DayOfTheMonth', 'DayOfTheWeek')
RepeatMode = enum(Weekly=2, Monthly=4, Yearly=8)
Names = enum('Sometime', 'Today', 'ThisWeek', 'ThisMonth', 'ThisYear', 'Yesterday', 'LastWeek', 'LastMonth', 'LastYear', 'Past', 'Tomorrow', 'NextWeek', 'NextMonth', 'NextYear', 'Future')
DaysOfWeek = {1: RepeatFlags.EveryMonday, 
   2: RepeatFlags.EveryTuesday, 
   3: RepeatFlags.EveryWednesday, 
   4: RepeatFlags.EveryThursday, 
   5: RepeatFlags.EveryFriday, 
   6: RepeatFlags.EverySaturday, 
   7: RepeatFlags.EverySunday}
DaysInMonth = {1: 31, 
   2: 28, 
   3: 31, 
   4: 30, 
   5: 31, 
   6: 30, 
   7: 31, 
   8: 31, 
   9: 30, 
   10: 31, 
   11: 30, 
   12: 31}

def addMonths(date, months):
    """
    Returns the new date based on the inputted months.
    
    :param      date   | <datetime.date>
                months | <int>
    
    :return     <datetime.date>
    """
    if type(date).__name__ in ('QDate', 'QDateTime', 'QTime'):
        date = date.toPython()
    mult = months / abs(months)
    years = mult * (abs(months) / 12)
    months = mult * (abs(months) % 12)
    month = date.month + months
    if month < 1:
        years -= 1
        month = 12 - month
    elif 12 < month:
        years += 1
        month %= 12
    year = date.year + years
    check = datetime.date(year, month, 1)
    days = daysInMonth(check)
    return datetime.date(year, month, min(date.day, days))


def addYears(date, years):
    """
    Returns the new date based on the inputted number of years.
    
    :param      date  | <datetime.date>
                years | <int>
    
    :return     <datetime.date>
    """
    if type(date).__name__ in ('QDate', 'QDateTime', 'QTime'):
        date = date.toPython()
    return datetime.date(date.year + years, date.month, date.day)


def daysInMonth(date):
    """
    Returns the number of the days in the month for the given date.  This will
    take into account leap years based on the inputted date's year.
    
    :param      date | <datetime.date>
    
    :return     <int>
    """
    if type(date).__name__ in ('QDate', 'QDateTime', 'QTime'):
        date = date.toPython()
    month = date.month
    if month == 2 and not date.year % 4:
        return 29
    return DaysInMonth.get(month, -1)


def daysInYear(date):
    """
    Returns the number of days in the year for the given date.
    
    :param      date | <datetime.date> || <int>
    
    :return     <int>
    """
    if type(date).__name__ in ('QDate', 'QDateTime', 'QTime'):
        date = date.toPython()
    if type(date) != int:
        year = date.year
    else:
        year = date
    if not year % 4:
        return 366
    return 365


def displayName(date, options=None, format='%b %d, %Y'):
    """
    Returns the display name for the inputted date, given the list of options.
    
    :param      date    | <datetime.date>
                options | <projex.dates.Names>
                format  | <str>
    
    :return     <str>
    """
    if type(date).__name__ in ('QDate', 'QDateTime', 'QTime'):
        date = date.toPython()
    if isinstance(date, datetime.datetime):
        time = ' @ ' + date.strftime('%I:%M%p').strip('0M').lower()
        date = date.date()
    else:
        time = ''
    today = datetime.date.today()
    delta = date - today
    if delta.days == 0:
        return 'Today' + time
    else:
        if delta.days == -1:
            return 'Yesterday' + time
        if delta.days == 1:
            return 'Tomorrow' + time
        if abs(delta.days) < 8:
            if date.isocalendar()[1] != today.isocalendar()[1]:
                qualifier = 'Last ' if delta.days < 0 else 'Next '
            else:
                qualifier = ''
            return qualifier + date.strftime('%A') + time
        return date.strftime(format)


def pretty(source, reference=None):
    reference = reference or datetime.datetime.now()

    def make_dtime(value):
        if type(value) == datetime.datetime:
            return value
        if type(value) == datetime.date:
            now = datetime.datetime.now()
            return datetime.datetime(value.year, value.month, value.day, now.hour, now.minute, now.second)
        if type(value) == datetime.time:
            today = datetime.date.today()
            return datetime.datetime(today.year, today.month, today.day, value.hour, value.minute, value.second)
        if type(value) == datetime.timedelta:
            return datetime.datetime.now() + value
        raise ValueError(source)

    use_time = type(source) != datetime.date
    source = make_dtime(source)
    reference = make_dtime(reference)
    reference.replace(tzinfo=source.tzinfo)
    delta = source - reference if reference < source else reference - source
    days = abs(delta.days)
    seconds = abs(delta.seconds)
    years = days / 365
    days %= 365
    months = days / 30
    days %= 30
    weeks = days / 7
    days %= 7
    parts = []
    suffix = 'ago' if source < reference else 'from now'
    if years == 1:
        parts.append('1 year')
    elif years > 1:
        parts.append(('{0} years').format(years))
    if months == 1:
        parts.append('1 month')
    elif months > 1:
        parts.append(('{0} months').format(months))
    if weeks == 1:
        parts.append('1 week')
    elif weeks > 1:
        parts.append(('{0} weeks').format(weeks))
    if days == 1:
        parts.append('1 day')
    elif days > 1:
        parts.append(('{0} days').format(days))
    if not use_time:
        if not parts:
            return 'today'
    elif seconds < 5:
        if not parts:
            return 'now'
    elif seconds < 60:
        parts.append(('{0} seconds').format(seconds))
    elif seconds < 120:
        parts.append('a minute')
    elif seconds < 3600:
        parts.append(('{0} minutes').format(seconds / 60))
    elif seconds < 7200:
        parts.append('an hour')
    else:
        parts.append(('{0} hours').format(seconds / 3600))
    if not parts:
        return source.strftime('%m/%d/%Y')
    else:
        return (', ').join(parts[:2]) + ' ' + suffix


def named(date, options=None):
    """
    Returns the best named option for the inputted date based on the inputted
    date name.
    
    :param      date    | <datetime.date>
                options | <projex.dates.Names> || None
    
    :return     <projex.dates.Names>
    """
    if type(date).__name__ in ('QDate', 'QDateTime', 'QTime'):
        date = date.toPython()
    if options is None:
        options = Names.all()
    if isinstance(date, datetime.datetime):
        date = date.date()
    today = datetime.date.today()
    today_month = today.month
    today_year, today_week, today_weekday = today.isocalendar()
    yesterday = today + datetime.timedelta(days=-1)
    tomorrow = today + datetime.timedelta(days=1)
    date_month = date.month
    date_year, date_week, date_weekday = date.isocalendar()
    if today == date and Names.Today & options:
        return Names.Today
    else:
        if yesterday == date and Names.Yesterday & options:
            return Names.Yesterday
        if tomorrow == date and Names.Tomorrow & options:
            return Names.Tomorrow
        if today_year == date_year:
            if today_month == date_month:
                if today_week == date_week and Names.ThisWeek & options:
                    return Names.ThisWeek
                if today_week == date_week + 1 and Names.LastWeek & options:
                    return Names.LastWeek
                if today_week == date_week - 1 and Names.NextWeek & options:
                    return Names.NextWeek
                if Names.ThisMonth & options:
                    return Names.ThisMonth
            else:
                if today_month == date_month + 1 and Names.LastMonth & options:
                    return Names.LastMonth
                if today_month == date_month - 1 and Names.NextMonth & options:
                    return Names.NextMonth
                if Names.ThisYear & options:
                    return Names.ThisYear
        else:
            if today_year == date_year + 1 and Names.LastYear & options:
                return Names.LastYear
            if today_year == date_year - 1 and Names.NextYear & options:
                return Names.NextYear
            if date < today and Names.Past & options:
                return Names.Past
            if today < date and Names.Future & options:
                return Names.Future
        return Names.Sometime


def repeating(first, mode=RepeatMode.Weekly, step=1, flags=0, startAt=None, repeatUntil=None, maximum=None):
    """
    Returns a list of repeating dates from the inputted start date based on the
    given mode.  If an repeatUntil date is supplied, then the results will be
    capped once the last date is reached, otherwise, the maximum number of
    results will be returned.
    
    :param      first       | <datetime.date>
                mode        | <RepeatMode>
                step        | <int> | value must be greater than 1
                flags       | <RepeatFlags>
                startAt     | <datetime.date> || None
                repeatUntil | <datetime.date> || None
                maximum     | <int> || None
    
    :return     [<datetime.date>, ..]
    """
    if repeatUntil is None and maximum is None:
        maximum = 100
    step = max(1, step)
    output = []
    if startAt is not None and first < startAt:
        if mode == RepeatMode.Monthly:
            curr = datetime.date(startAt.year, startAt.month, first.day)
        elif mode == RepeatMode.Yearly:
            curr = datetime.date(startAt.year, first.month, first.day)
        else:
            curr = first
    else:
        curr = first
    if curr < first:
        curr = first
    any_days = 0
    for value in DaysOfWeek.values():
        any_days |= value

    while True:
        if mode == RepeatMode.Weekly:
            if flags & any_days:
                start = curr + datetime.timedelta(days=1 - curr.isoweekday())
                exit_loop = False
                for i in range(7):
                    day = start + datetime.timedelta(days=i)
                    if day < first:
                        continue
                    elif repeatUntil is not None and repeatUntil < day:
                        exit_loop = True
                        break
                    flag = DaysOfWeek[day.isoweekday()]
                    if not flags & flag:
                        continue
                    if startAt is None or startAt <= day:
                        output.append(day)

                if exit_loop:
                    break
            else:
                if repeatUntil is not None and repeatUntil < curr:
                    break
                if startAt is None or startAt <= curr:
                    output.append(curr)
            curr = curr + datetime.timedelta(days=7 * step)
        if repeatUntil is not None and repeatUntil < curr:
            break
        elif maximum is not None and len(output) == maximum:
            break
        elif mode == RepeatMode.Weekly:
            if startAt is None or startAt <= curr:
                output.append(curr)
            curr = curr + datetime.timedelta(days=step * 7)
        elif mode == RepeatMode.Monthly:
            if startAt is None or startAt <= curr:
                output.append(curr)
            curr = addMonths(curr, step)
            if flags & RepeatFlags.DayOfTheWeek != 0:
                shift = curr.isodayofweek() - first.isoweekday()
                curr = curr + datetime.timedelta(days=shift)
        elif mode == RepeatMode.Yearly:
            if startAt is None or startAt <= curr:
                output.append(curr)
            curr = addYears(curr, step)

    return output


def weekdays(start, end):
    """
    Returns the number of weekdays between the inputted start and end dates.
    This would be the equivalent of doing (end - start) to get the number of
    calendar days between the two dates.
    
    :param      start | <datetime.date>
                end   | <datetime.date>
    
    :return     <int>
    """
    if start == end:
        return int(start.isoweekday() not in (6, 7))
    else:
        if end < start:
            return -weekdays(end, start)
        strt_weekday = start.isoweekday()
        end_weekday = end.isoweekday()
        if end < start:
            return -weekdays(end, start)
        if 5 < strt_weekday:
            start = start + datetime.timedelta(days=8 - strt_weekday)
        if 5 < end_weekday:
            end = end - datetime.timedelta(days=end_weekday - 5)
        remainder = end.isoweekday() - start.isoweekday()
        end = end - datetime.timedelta(days=remainder)
        if end < start:
            return 0
        if end == start:
            return remainder + 1
        days = (end - start).days + 1
        total_days = abs(days)
        multiplier = days / total_days
        weekends = int(round(total_days / 7.0) * 2)
        week_days = (total_days - weekends + remainder) * multiplier
        return week_days