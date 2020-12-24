# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/parsing/date_utils.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 5248 bytes
import datetime
from datetime import timedelta
import dateutil.parser, pytz
from celery.utils.log import get_task_logger
from dateutil.relativedelta import relativedelta
from django.utils import timezone
logger = get_task_logger(__name__)

def process_datetime(values, duration=None):
    """
    Output example:
        Q: next_week: (datetime.datetime(2016, 11, 21, 0, 0, tzinfo=tzoffset(None, 3600)), datetime.datetime(2016, 11, 28, 0, 0, tzinfo=tzoffset(None, 3600)))
        Q: tomorrow: (datetime.datetime(2016, 11, 18, 0, 0, tzinfo=tzoffset(None, 3600)), datetime.datetime(2016, 11, 19, 0, 0, tzinfo=tzoffset(None, 3600)))
        Q: tonight: (datetime.datetime(2016, 11, 17, 18, 0, tzinfo=tzoffset(None, 3600)), datetime.datetime(2016, 11, 18, 0, 0, tzinfo=tzoffset(None, 3600)))
        Q: at weekend: (datetime.datetime(2016, 11, 18, 18, 0, tzinfo=tzoffset(None, 3600)), datetime.datetime(2016, 11, 21, 0, 0, tzinfo=tzoffset(None, 3600)))
    """
    append = {'date_interval': []}
    for value in values:
        try:
            formatted = None
            if value['type'] == 'interval':
                if 'from' not in value:
                    date_from = datetime.datetime.now().replace(tzinfo=(pytz.timezone('Europe/Prague')))
                else:
                    date_from = dateutil.parser.parse(value['from']['value'])
                date_to = dateutil.parser.parse(value['to']['value']) - timedelta(seconds=1)
                grain = value['from']['grain']
            else:
                grain = value['grain']
                date_from = dateutil.parser.parse(value['value'])
                if grain == 'week':
                    if date_from == date_this_week(date_from.tzinfo):
                        date_from = timezone.now()
                        formatted = 'the next seven days'
                date_to = date_from + timedelta_from_grain(grain)
                if 'datetime' not in append:
                    append['datetime'] = []
                append['datetime'].append({'value':date_from,  'grain':grain})
            if not formatted:
                formatted = format_date_interval(date_from, date_to, grain)
            append['date_interval'].append({'value':(date_from, date_to),  'grain':grain,  'formatted':formatted})
        except ValueError:
            logger.exception('Error parsing date: {}'.format(value))

    return append


def timedelta_from_grain(grain):
    if grain == 'second':
        return timedelta(seconds=1)
    else:
        if grain == 'minute':
            return timedelta(minutes=1)
        else:
            if grain == 'hour':
                return timedelta(hours=1)
            else:
                if grain == 'day':
                    return timedelta(days=1)
                if grain == 'week':
                    return timedelta(days=7)
                if grain == 'month':
                    return timedelta(days=31)
            if grain == 'year':
                return timedelta(days=365)
        return timedelta(days=1)


def date_now(tzinfo):
    return datetime.datetime.now(tzinfo)


def date_today(tzinfo):
    return date_now(tzinfo).replace(hour=0, minute=0, second=0, microsecond=0)


def date_this_week(tzinfo):
    today = date_today(tzinfo)
    return today - timedelta(days=(today.weekday()))


def date_this_month(tzinfo):
    today = date_today(tzinfo)
    return today - timedelta(days=(today.day - 1))


def format_date_interval(from_date, to_date, grain):
    tzinfo = from_date.tzinfo
    now = date_now(tzinfo)
    today = date_today(tzinfo)
    this_week = date_this_week(tzinfo)
    next_week = this_week + timedelta(days=7)
    this_month = date_this_month(tzinfo)
    next_month = date_this_month(tzinfo) + relativedelta(months=1)
    diff_hours = (to_date - from_date).total_seconds() / 3600
    logger.info('Diff hours: %s' % diff_hours)
    if grain in ('second', 'minute'):
        if (now - from_date).total_seconds() < 300:
            return 'now'
    for i in range(0, 6):
        if from_date >= today + timedelta(days=i) and to_date <= today + timedelta(days=(i + 1)):
            if i == 0:
                day = 'today'
            else:
                if i == 1:
                    day = 'tomorrow'
                else:
                    day = '%s' % from_date.strftime('%A')
                if from_date.hour >= 17:
                    if i == 0:
                        return 'this evening'
                    return day + ' evening'
                else:
                    if from_date.hour >= 12:
                        if i == 0:
                            return 'this afternoon'
                        else:
                            return day + ' afternoon'
                    else:
                        if to_date.hour >= 0:
                            if to_date.hour < 13:
                                if to_date.hour > 0:
                                    if i == 0:
                                        return 'this morning'
                                    else:
                                        return day + ' morning'
                    return day

    if from_date == this_week:
        if to_date == next_week:
            return 'this week'
    if from_date == next_week:
        if to_date == next_week + timedelta(days=7):
            return 'next week'
    if from_date == this_month:
        if to_date == next_month:
            return 'this month'
    if diff_hours <= 25:
        digit = from_date.day % 10
        date = 'the {}{}'.format(from_date.day, 'st' if digit == 1 else 'nd' if digit == 2 else 'th')
        if from_date.month == now.month:
            return date
        return date + ' ' + from_date.strftime('%B')
    else:
        return 'these dates'