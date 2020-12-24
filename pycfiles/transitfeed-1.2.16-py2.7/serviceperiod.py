# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/transitfeed/serviceperiod.py
# Compiled at: 2018-01-24 00:52:58
import datetime, re, time, problems as problems_module, util

class ServicePeriod(object):
    """Represents a service, which identifies a set of dates when one or more
  trips operate."""
    _DAYS_OF_WEEK = [
     'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
     'saturday', 'sunday']
    _REQUIRED_FIELD_NAMES = [
     'service_id', 'start_date', 'end_date'] + _DAYS_OF_WEEK
    _FIELD_NAMES = _REQUIRED_FIELD_NAMES
    _DEPRECATED_FIELD_NAMES = []
    _REQUIRED_FIELD_NAMES_CALENDAR_DATES = ['service_id', 'date',
     'exception_type']
    _FIELD_NAMES_CALENDAR_DATES = _REQUIRED_FIELD_NAMES_CALENDAR_DATES
    _DEPRECATED_FIELD_NAMES_CALENDAR_DATES = []
    _VALID_DATE_RANGE_FROM = 1900
    _VALID_DATE_RANGE_TO = 2100
    _EXCEPTION_TYPE_ADD = 1
    _EXCEPTION_TYPE_REMOVE = 2

    def __init__(self, id=None, field_list=None):
        self.original_day_values = []
        if field_list:
            self.service_id = field_list[self._FIELD_NAMES.index('service_id')]
            self.day_of_week = [False] * len(self._DAYS_OF_WEEK)
            for day in self._DAYS_OF_WEEK:
                value = field_list[self._FIELD_NAMES.index(day)] or ''
                self.original_day_values += [value.strip()]
                self.day_of_week[self._DAYS_OF_WEEK.index(day)] = value == '1'

            self.start_date = field_list[self._FIELD_NAMES.index('start_date')]
            self.end_date = field_list[self._FIELD_NAMES.index('end_date')]
        else:
            self.service_id = id
            self.day_of_week = [False] * 7
            self.start_date = None
            self.end_date = None
        self.date_exceptions = {}
        return

    def HasExceptions(self):
        """Checks if the ServicePeriod has service exceptions."""
        if self.date_exceptions:
            return True
        else:
            return False

    def GetDateRange(self):
        """Return the range over which this ServicePeriod is valid.

    The range includes exception dates that add service outside of
    (start_date, end_date), but doesn't shrink the range if exception
    dates take away service at the edges of the range.

    Returns:
      A tuple of "YYYYMMDD" strings, (start date, end date) or (None, None) if
      no dates have been given.
    """
        start = self.start_date
        end = self.end_date
        for date, (exception_type, _) in self.date_exceptions.items():
            if exception_type == self._EXCEPTION_TYPE_REMOVE:
                continue
            if not start or date < start:
                start = date
            if not end or date > end:
                end = date

        if start is None:
            start = end
        elif end is None:
            end = start
        return (start, end)

    def GetCalendarFieldValuesTuple(self):
        """Return the tuple of calendar.txt values or None if this ServicePeriod
    should not be in calendar.txt ."""
        if self.start_date and self.end_date:
            return [ getattr(self, fn) for fn in self._FIELD_NAMES ]

    def GenerateCalendarDatesFieldValuesTuples(self):
        """Generates tuples of calendar_dates.txt values. Yield zero tuples if
    this ServicePeriod should not be in calendar_dates.txt ."""
        for date, (exception_type, _) in self.date_exceptions.items():
            yield (
             self.service_id, date, unicode(exception_type))

    def GetCalendarDatesFieldValuesTuples(self):
        """Return a list of date execeptions"""
        result = []
        for date_tuple in self.GenerateCalendarDatesFieldValuesTuples():
            result.append(date_tuple)

        result.sort()
        return result

    def SetDateHasService(self, date, has_service=True, problems=None):
        if date in self.date_exceptions and problems:
            problems.DuplicateID(('service_id', 'date'), (
             self.service_id, date), type=problems_module.TYPE_WARNING)
        exception_context_tuple = (has_service and self._EXCEPTION_TYPE_ADD or self._EXCEPTION_TYPE_REMOVE,
         problems != None and problems.GetFileContext() or None)
        self.date_exceptions[date] = exception_context_tuple
        return

    def ResetDateToNormalService(self, date):
        if date in self.date_exceptions:
            del self.date_exceptions[date]

    def SetStartDate(self, start_date):
        """Set the first day of service as a string in YYYYMMDD format"""
        self.start_date = start_date

    def SetEndDate(self, end_date):
        """Set the last day of service as a string in YYYYMMDD format"""
        self.end_date = end_date

    def SetDayOfWeekHasService(self, dow, has_service=True):
        """Set service as running (or not) on a day of the week. By default the
    service does not run on any days.

    Args:
      dow: 0 for Monday through 6 for Sunday
      has_service: True if this service operates on dow, False if it does not.

    Returns:
      None
    """
        assert dow >= 0 and dow < 7
        self.day_of_week[dow] = has_service

    def SetWeekdayService(self, has_service=True):
        """Set service as running (or not) on all of Monday through Friday."""
        for i in range(0, 5):
            self.SetDayOfWeekHasService(i, has_service)

    def SetWeekendService(self, has_service=True):
        """Set service as running (or not) on Saturday and Sunday."""
        self.SetDayOfWeekHasService(5, has_service)
        self.SetDayOfWeekHasService(6, has_service)

    def SetServiceId(self, service_id):
        """Set the service_id for this schedule. Generally the default will
    suffice so you won't need to call this method."""
        self.service_id = service_id

    def HasDateExceptionOn(self, date, exception_type=_EXCEPTION_TYPE_ADD):
        """Test if this service period has a date exception of the given type.

    Args:
      date: a string of form "YYYYMMDD"
      exception_type: the exception type the date should have. Defaults to
                      _EXCEPTION_TYPE_ADD

    Returns:
      True iff this service has service exception of specified type at date.
    """
        if date in self.date_exceptions:
            return exception_type == self.date_exceptions[date][0]
        return False

    def IsActiveOn(self, date, date_object=None):
        """Test if this service period is active on a date.

    Args:
      date: a string of form "YYYYMMDD"
      date_object: a date object representing the same date as date.
                   This parameter is optional, and present only for performance
                   reasons.
                   If the caller constructs the date string from a date object
                   that date object can be passed directly, thus avoiding the
                   costly conversion from string to date object.

    Returns:
      True iff this service is active on date.
    """
        if date in self.date_exceptions:
            exception_type, _ = self.date_exceptions[date]
            if exception_type == self._EXCEPTION_TYPE_ADD:
                return True
            return False
        if self.start_date and self.end_date and self.start_date <= date and date <= self.end_date:
            if date_object is None:
                date_object = util.DateStringToDateObject(date)
            return self.day_of_week[date_object.weekday()]
        else:
            return False

    def ActiveDates(self):
        """Return dates this service period is active as a list of "YYYYMMDD"."""
        earliest, latest = self.GetDateRange()
        if earliest is None:
            return []
        else:
            dates = []
            date_it = util.DateStringToDateObject(earliest)
            date_end = util.DateStringToDateObject(latest)
            delta = datetime.timedelta(days=1)
            while date_it <= date_end:
                date_it_string = date_it.strftime('%Y%m%d')
                if self.IsActiveOn(date_it_string, date_it):
                    dates.append(date_it_string)
                date_it = date_it + delta

            return dates

    def __getattr__(self, name):
        try:
            return self.day_of_week[self._DAYS_OF_WEEK.index(name)] and 1 or 0
        except KeyError:
            pass
        except ValueError:
            pass

        raise AttributeError(name)

    def __getitem__(self, name):
        return getattr(self, name)

    def __eq__(self, other):
        if not other:
            return False
        if id(self) == id(other):
            return True
        if self.GetCalendarFieldValuesTuple() != other.GetCalendarFieldValuesTuple():
            return False
        if self.GetCalendarDatesFieldValuesTuples() != other.GetCalendarDatesFieldValuesTuples():
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def ValidateServiceId(self, problems):
        if util.IsEmpty(self.service_id):
            problems.MissingValue('service_id')

    def ValidateStartDate(self, problems):
        if not self.ValidateDate(self.start_date, 'start_date', problems):
            self.start_date = None
        return

    def ValidateEndDate(self, problems):
        if not self.ValidateDate(self.end_date, 'end_date', problems):
            self.end_date = None
        return

    def ValidateEndDateAfterStartDate(self, problems):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            problems.InvalidValue('end_date', self.end_date, 'end_date of %s is earlier than start_date of "%s"' % (
             self.end_date, self.start_date))

    def ValidateDaysOfWeek(self, problems):
        if self.original_day_values:
            index = 0
            for value in self.original_day_values:
                column_name = self._DAYS_OF_WEEK[index]
                if util.IsEmpty(value):
                    problems.MissingValue(column_name)
                elif value != '0' and value != '1':
                    problems.InvalidValue(column_name, value)
                index += 1

    def ValidateHasServiceAtLeastOnceAWeek(self, problems):
        if True not in self.day_of_week and not self.HasDateExceptionTypeAdded():
            problems.OtherProblem('Service period with service_id "%s" doesn\'t have service on any days of the week.' % self.service_id, type=problems_module.TYPE_WARNING)

    def HasDateExceptionTypeAdded(self):
        for exception_type, _ in self.date_exceptions.values():
            if exception_type == self._EXCEPTION_TYPE_ADD:
                return True

        return False

    def ValidateDates(self, problems):
        for date, (exception_type, context) in self.date_exceptions.items():
            self.ValidateDate(date, 'date', problems, context)

    def ValidateDate(self, date, field_name, problems, context=None):
        if date is None:
            return False
        else:
            if util.IsEmpty(date):
                problems.MissingValue(field_name, date, context)
                return False
            if not util.ValidateDate(date, field_name, problems):
                return False
            try:
                date_value = time.strptime(date, '%Y%m%d')
                if not self._VALID_DATE_RANGE_FROM <= date_value.tm_year <= self._VALID_DATE_RANGE_TO:
                    problems.DateOutsideValidRange(field_name, date, self._VALID_DATE_RANGE_FROM, self._VALID_DATE_RANGE_TO, context=context)
                    return False
                return True
            except ValueError:
                problems.InvalidValue(field_name, 'Could not parse date value.', date, context, problems_module.TYPE_ERROR)
                return False

            return

    def Validate(self, problems=problems_module.default_problem_reporter):
        self.ValidateServiceId(problems)
        self.ValidateStartDate(problems)
        self.ValidateEndDate(problems)
        self.ValidateEndDateAfterStartDate(problems)
        self.ValidateDaysOfWeek(problems)
        self.ValidateHasServiceAtLeastOnceAWeek(problems)
        self.ValidateDates(problems)