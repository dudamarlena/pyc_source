# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weekdays/helpers.py
# Compiled at: 2013-11-06 10:03:24
import datetime
from weekdays import get_business_days
import calendar

class BusinessCalendar(calendar.Calendar):

    def __init__(self, weekstartday, weekoff, holidays):
        self.weekstartday = weekstartday
        self.weekoff = weekoff
        self.holidays = holidays
        super(BusinessCalendar, self).__init__(weekstartday)

    def get_month_business_days(self, year, month):
        """given a year and a month returns the business days for this month
        respecting the rules that were give during calendar initialisation.
        """
        start = datetime.datetime(year, month, 1, 0, 0)
        lastdaynum = calendar.monthrange(year, month)[1]
        end = datetime.datetime(year, month, lastdaynum, 0, 0)
        return get_business_days(start, end, self.weekoff, self.holidays)

    def get_weeks_business_days(self, year, month):
        """given an year and month returns the business days for this month
        ordered in lists of weeks.
        """
        business_weeks = []
        allweeksdays = self.monthdatescalendar(year, month)
        monthbusinessdays = self.get_month_business_days(year, month)
        for week in allweeksdays:
            weekbusinessdays = []
            for day in week:
                daydt = datetime.datetime(day.year, day.month, day.day, 0, 0)
                if daydt in monthbusinessdays:
                    weekbusinessdays.append(daydt)

            business_weeks.append(weekbusinessdays)

        return business_weeks

    def get_weeks_daycount(self, year, month):
        """given a year and month returns a list of business days count
        for all the weeks of the month.
        ie: [0, 5, 4, 5, 5]
        """
        return [ len(week) for week in self.get_weeks_business_days(year, month) ]