# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/transitfeed/frequency.py
# Compiled at: 2018-01-24 00:52:58
from gtfsobjectbase import GtfsObjectBase
import util

class Frequency(GtfsObjectBase):
    """This class represents a period of a trip during which the vehicle travels
    at regular intervals (rather than specifying exact times for each stop)."""
    _REQUIRED_FIELD_NAMES = [
     'trip_id', 'start_time', 'end_time',
     'headway_secs']
    _FIELD_NAMES = _REQUIRED_FIELD_NAMES + ['exact_times']
    _TABLE_NAME = 'frequencies'

    def __init__(self, field_dict=None):
        self._schedule = None
        if field_dict:
            if isinstance(field_dict, self.__class__):
                for k, v in field_dict.iteritems():
                    self.__dict__[k] = v

            else:
                self.__dict__.update(field_dict)
        return

    def StartTime(self):
        return self.start_time

    def EndTime(self):
        return self.end_time

    def TripId(self):
        return self.trip_id

    def HeadwaySecs(self):
        return self.headway_secs

    def ExactTimes(self):
        return self.exact_times

    def ValidateExactTimes(self, problems):
        if util.IsEmpty(self.exact_times):
            self.exact_times = 0
            return
        try:
            self.exact_times = int(self.exact_times)
        except (ValueError, TypeError):
            problems.InvalidValue('exact_times', self.exact_times, 'Should be 0 (no fixed schedule) or 1 (fixed and regular schedule, shortcut for a repetitive stop_times file).')
            del self.exact_times
            return

        if self.exact_times not in (0, 1):
            problems.InvalidValue('exact_times', self.exact_times, 'Should be 0 (no fixed schedule) or 1 (fixed and regular schedule, shortcut for a repetitive stop_times file).')

    def ValidateBeforeAdd(self, problems):
        self.ValidateExactTimes(problems)
        return True

    def ValidateAfterAdd(self, problems):
        pass

    def Validate(self, problems=None):
        returns

    def AddToSchedule(self, schedule=None, problems=None):
        if schedule is None:
            return
        else:
            self._schedule = schedule
            try:
                trip = schedule.GetTrip(self.trip_id)
            except KeyError:
                problems.InvalidValue('trip_id', self.trip_id)
                return

            trip.AddFrequencyObject(self, problems)
            return