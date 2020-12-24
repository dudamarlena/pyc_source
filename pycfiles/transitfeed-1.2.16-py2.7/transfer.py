# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/transitfeed/transfer.py
# Compiled at: 2018-01-24 00:52:58
from gtfsobjectbase import GtfsObjectBase
import problems as problems_module, util

class Transfer(GtfsObjectBase):
    """Represents a transfer in a schedule"""
    _REQUIRED_FIELD_NAMES = [
     'from_stop_id', 'to_stop_id', 'transfer_type']
    _FIELD_NAMES = _REQUIRED_FIELD_NAMES + ['min_transfer_time']
    _TABLE_NAME = 'transfers'
    _ID_COLUMNS = ['from_stop_id', 'to_stop_id']

    def __init__(self, schedule=None, from_stop_id=None, to_stop_id=None, transfer_type=None, min_transfer_time=None, field_dict=None):
        self._schedule = None
        if field_dict:
            self.__dict__.update(field_dict)
        else:
            self.from_stop_id = from_stop_id
            self.to_stop_id = to_stop_id
            self.transfer_type = transfer_type
            self.min_transfer_time = min_transfer_time
        if getattr(self, 'transfer_type', None) in ('', None):
            self.transfer_type = 0
        else:
            try:
                self.transfer_type = util.NonNegIntStringToInt(self.transfer_type)
            except (TypeError, ValueError):
                pass

        if hasattr(self, 'min_transfer_time'):
            try:
                self.min_transfer_time = util.NonNegIntStringToInt(self.min_transfer_time)
            except (TypeError, ValueError):
                pass

        else:
            self.min_transfer_time = None
        if schedule is not None:
            schedule.AddTransferObject(self)
        return

    def ValidateFromStopIdIsPresent(self, problems):
        if util.IsEmpty(self.from_stop_id):
            problems.MissingValue('from_stop_id')
            return False
        return True

    def ValidateToStopIdIsPresent(self, problems):
        if util.IsEmpty(self.to_stop_id):
            problems.MissingValue('to_stop_id')
            return False
        return True

    def ValidateTransferType(self, problems):
        if not util.IsEmpty(self.transfer_type):
            if not isinstance(self.transfer_type, int) or self.transfer_type not in range(0, 4):
                problems.InvalidValue('transfer_type', self.transfer_type)
                return False
        return True

    def ValidateMinimumTransferTime(self, problems):
        if not util.IsEmpty(self.min_transfer_time):
            if self.transfer_type != 2:
                problems.MinimumTransferTimeSetWithInvalidTransferType(self.transfer_type)
            if isinstance(self.min_transfer_time, int):
                if self.min_transfer_time < 0:
                    problems.InvalidValue('min_transfer_time', self.min_transfer_time, reason='This field cannot contain a negative value.')
                elif self.min_transfer_time >= 86400:
                    problems.InvalidValue('min_transfer_time', self.min_transfer_time, reason='The value is very large for a transfer time and most likely indicates an error.')
                elif self.min_transfer_time >= 10800:
                    problems.InvalidValue('min_transfer_time', self.min_transfer_time, type=problems_module.TYPE_WARNING, reason='The value is large for a transfer time and most likely indicates an error.')
            else:
                problems.InvalidValue('min_transfer_time', self.min_transfer_time, reason='If present, this field should contain an integer value.')
                return False
        return True

    def GetTransferDistance(self):
        from_stop = self._schedule.stops[self.from_stop_id]
        to_stop = self._schedule.stops[self.to_stop_id]
        distance = util.ApproximateDistanceBetweenStops(from_stop, to_stop)
        return distance

    def ValidateFromStopIdIsValid(self, problems):
        if self.from_stop_id not in self._schedule.stops.keys():
            problems.InvalidValue('from_stop_id', self.from_stop_id)
            return False
        return True

    def ValidateToStopIdIsValid(self, problems):
        if self.to_stop_id not in self._schedule.stops.keys():
            problems.InvalidValue('to_stop_id', self.to_stop_id)
            return False
        return True

    def ValidateTransferDistance(self, problems):
        distance = self.GetTransferDistance()
        if distance > 10000:
            problems.TransferDistanceTooBig(self.from_stop_id, self.to_stop_id, distance)
        elif distance > 2000:
            problems.TransferDistanceTooBig(self.from_stop_id, self.to_stop_id, distance, type=problems_module.TYPE_WARNING)

    def ValidateTransferWalkingTime(self, problems):
        if util.IsEmpty(self.min_transfer_time):
            return
        if self.min_transfer_time < 0:
            return
        distance = self.GetTransferDistance()
        FAST_WALKING_SPEED = 2
        if self.min_transfer_time + 120 < distance / FAST_WALKING_SPEED:
            problems.TransferWalkingSpeedTooFast(from_stop_id=self.from_stop_id, to_stop_id=self.to_stop_id, transfer_time=self.min_transfer_time, distance=distance)

    def ValidateBeforeAdd(self, problems):
        result = True
        result = self.ValidateFromStopIdIsPresent(problems) and result
        result = self.ValidateToStopIdIsPresent(problems) and result
        result = self.ValidateTransferType(problems) and result
        result = self.ValidateMinimumTransferTime(problems) and result
        return result

    def ValidateAfterAdd(self, problems):
        valid_stop_ids = True
        valid_stop_ids = self.ValidateFromStopIdIsValid(problems) and valid_stop_ids
        valid_stop_ids = self.ValidateToStopIdIsValid(problems) and valid_stop_ids
        if valid_stop_ids:
            self.ValidateTransferDistance(problems)
            self.ValidateTransferWalkingTime(problems)

    def Validate(self, problems=problems_module.default_problem_reporter):
        if self.ValidateBeforeAdd(problems) and self._schedule:
            self.ValidateAfterAdd(problems)

    def _ID(self):
        return tuple(self[i] for i in self._ID_COLUMNS)

    def AddToSchedule(self, schedule, problems):
        schedule.AddTransferObject(self, problems)