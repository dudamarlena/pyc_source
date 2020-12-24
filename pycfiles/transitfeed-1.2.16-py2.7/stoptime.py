# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/transitfeed/stoptime.py
# Compiled at: 2018-01-24 00:52:58
import problems as problems_module
from stop import Stop
import util

class StopTime(object):
    """
  Represents a single stop of a trip. StopTime contains most of the columns
  from the stop_times.txt file. It does not contain trip_id, which is implied
  by the Trip used to access it.

  See the Google Transit Feed Specification for the semantic details.

  stop: A Stop object
  arrival_time: str in the form HH:MM:SS; readonly after __init__
  departure_time: str in the form HH:MM:SS; readonly after __init__
  arrival_secs: int number of seconds since midnight
  departure_secs: int number of seconds since midnight
  stop_headsign: str
  pickup_type: int
  drop_off_type: int
  shape_dist_traveled: float
  stop_id: str; readonly
  stop_time: The only time given for this stop.  If present, it is used
             for both arrival and departure time.
  stop_sequence: int
  timepoint: int
  """
    _REQUIRED_FIELD_NAMES = [
     'trip_id', 'arrival_time', 'departure_time',
     'stop_id', 'stop_sequence']
    _OPTIONAL_FIELD_NAMES = ['stop_headsign', 'pickup_type',
     'drop_off_type', 'shape_dist_traveled', 'timepoint']
    _FIELD_NAMES = _REQUIRED_FIELD_NAMES + _OPTIONAL_FIELD_NAMES
    _DEPRECATED_FIELD_NAMES = []
    _SQL_FIELD_NAMES = ['trip_id', 'arrival_secs', 'departure_secs',
     'stop_id', 'stop_sequence', 'stop_headsign',
     'pickup_type', 'drop_off_type', 'shape_dist_traveled',
     'timepoint']
    _STOP_CLASS = Stop
    __slots__ = ('arrival_secs', 'departure_secs', 'stop', 'stop_headsign', 'pickup_type',
                 'drop_off_type', 'shape_dist_traveled', 'stop_sequence', 'timepoint')

    def __init__(self, problems, stop, arrival_time=None, departure_time=None, stop_headsign=None, pickup_type=None, drop_off_type=None, shape_dist_traveled=None, arrival_secs=None, departure_secs=None, stop_time=None, stop_sequence=None, timepoint=None):
        if stop_time != None:
            arrival_time = departure_time = stop_time
        if arrival_secs != None:
            self.arrival_secs = arrival_secs
        else:
            if arrival_time in (None, ''):
                self.arrival_secs = None
                arrival_time = None
            else:
                try:
                    self.arrival_secs = util.TimeToSecondsSinceMidnight(arrival_time)
                except problems_module.Error:
                    problems.InvalidValue('arrival_time', arrival_time)
                    self.arrival_secs = None

            if departure_secs != None:
                self.departure_secs = departure_secs
            elif departure_time in (None, ''):
                self.departure_secs = None
                departure_time = None
            else:
                try:
                    self.departure_secs = util.TimeToSecondsSinceMidnight(departure_time)
                except problems_module.Error:
                    problems.InvalidValue('departure_time', departure_time)
                    self.departure_secs = None

            if not isinstance(stop, self._STOP_CLASS):
                problems.InvalidValue('stop', stop)
            self.stop = stop
            self.stop_headsign = stop_headsign
            self.timepoint = util.ValidateAndReturnIntValue(timepoint, [0, 1], None, True, 'timepoint', problems)
            self.pickup_type = util.ValidateAndReturnIntValue(pickup_type, [0, 1, 2, 3], None, True, 'pickup_type', problems)
            self.drop_off_type = util.ValidateAndReturnIntValue(drop_off_type, [0, 1, 2, 3], None, True, 'drop_off_type', problems)
            if self.pickup_type == 1 and self.drop_off_type == 1 and self.arrival_secs == None and self.departure_secs == None:
                problems.OtherProblem("This stop time has a pickup_type and drop_off_type of 1, indicating that riders can't get on or off here.  Since it doesn't define a timepoint either, this entry serves no purpose and should be excluded from the trip.", type=problems_module.TYPE_WARNING)
            if self.arrival_secs != None and self.departure_secs != None and self.departure_secs < self.arrival_secs:
                problems.InvalidValue('departure_time', departure_time, "The departure time at this stop (%s) is before the arrival time (%s).  This is often caused by problems in the feed exporter's time conversion" % (
                 departure_time, arrival_time))
            if self.arrival_secs != None and self.departure_secs == None and departure_time == None:
                problems.MissingValue('departure_time', "arrival_time and departure_time should either both be provided or both be left blank.  It's OK to set them both to the same value.")
            if self.departure_secs != None and self.arrival_secs == None and arrival_time == None:
                problems.MissingValue('arrival_time', "arrival_time and departure_time should either both be provided or both be left blank.  It's OK to set them both to the same value.")
            if shape_dist_traveled in (None, ''):
                self.shape_dist_traveled = None
            else:
                try:
                    self.shape_dist_traveled = float(shape_dist_traveled)
                except ValueError:
                    problems.InvalidValue('shape_dist_traveled', shape_dist_traveled)

        if stop_sequence is not None:
            self.stop_sequence = stop_sequence
        return

    def GetFieldValuesTuple(self, trip_id):
        """Return a tuple that outputs a row of _FIELD_NAMES to be written to a
       GTFS file.

    Arguments:
        trip_id: The trip_id of the trip to which this StopTime corresponds.
                 It must be provided, as it is not stored in StopTime.
    """
        result = []
        for fn in self._FIELD_NAMES:
            if fn == 'trip_id':
                result.append(trip_id)
            else:
                result.append(getattr(self, fn) or '')

        return tuple(result)

    def GetSqlValuesTuple(self, trip_id):
        """Return a tuple that outputs a row of _FIELD_NAMES to be written to a
       SQLite database.

    Arguments:
        trip_id: The trip_id of the trip to which this StopTime corresponds.
                 It must be provided, as it is not stored in StopTime.
    """
        result = []
        for fn in self._SQL_FIELD_NAMES:
            if fn == 'trip_id':
                result.append(trip_id)
            else:
                result.append(getattr(self, fn))

        return tuple(result)

    def GetTimeSecs(self):
        """Return the first of arrival_secs and departure_secs that is not None.
    If both are None return None."""
        if self.arrival_secs != None:
            return self.arrival_secs
        else:
            if self.departure_secs != None:
                return self.departure_secs
            else:
                return

            return

    def __getattr__(self, name):
        if name == 'stop_id':
            return self.stop.stop_id
        else:
            if name == 'arrival_time':
                return self.arrival_secs != None and util.FormatSecondsSinceMidnight(self.arrival_secs) or ''
            if name == 'departure_time':
                return self.departure_secs != None and util.FormatSecondsSinceMidnight(self.departure_secs) or ''
            if name == 'shape_dist_traveled':
                return ''
            raise AttributeError(name)
            return