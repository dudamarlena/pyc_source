# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weekdays/main.py
# Compiled at: 2014-06-13 11:04:19
from dateutil import rrule
import datetime

def get_business_days(alpha, omega, weekoff=None, holidays=None):
    """return a list of business days between (inclusive) the
    from and to limits.
    @type alpha: datetime.datetime
    @type omega: datetime.datetime
    @param weekoff: a list of non working days in a normal week
    @type weekend: list of rrule.weekdays. Ex: [rrule.SA, rrule.SU]
    @param holidays: a list of special non working days
    @type holidays: list of rrule args or dates.
        ex: [{'freq':dateutil.rrule.YEARLY, 'bymonthday':1, 'bymonth':11}]
    """
    dates = rrule.rruleset()
    dates.rrule(rrule.rrule(rrule.DAILY, dtstart=alpha, until=omega))
    if weekoff:
        dates.exrule(rrule.rrule(rrule.DAILY, byweekday=weekoff, dtstart=alpha))
    if holidays:
        for holiday in holidays:
            if isinstance(holiday, datetime.datetime):
                dates.exdate(holiday)
            else:
                complete_holiday = {}
                for key in holiday:
                    complete_holiday[key] = holiday[key]

                complete_holiday['dtstart'] = alpha
                dates.exrule(rrule.rrule(**complete_holiday))

    return list(dates)