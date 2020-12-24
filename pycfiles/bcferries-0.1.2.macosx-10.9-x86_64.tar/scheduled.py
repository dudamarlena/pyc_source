# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yasyf/.virtualenvs/bcferries/lib/python2.7/site-packages/bcferries/scheduled.py
# Compiled at: 2014-12-30 23:30:23
from abstract import BCFerriesAbstractObject
from helpers import to_int
import dateutil.parser, datetime, re
time_regex = re.compile('(\\d) HOURS?(?: (\\d{1,2}) MINUTES?)?')

class BCFerriesScheduledCrossing(BCFerriesAbstractObject):

    def __init__(self, name, sailing_time, time_row):
        super(BCFerriesScheduledCrossing, self).__init__(self)
        scheduled_dep, actual_dep, arrival, status, _ = time_row
        self.boat_name = name
        self.name = ('{} at {}').format(name, scheduled_dep)
        self.status = status.strip()
        self.sailing_time = 0
        match = time_regex.match(sailing_time)
        if match:
            hours, minutes = match.group(1, 2)
            self.sailing_time = datetime.timedelta(minutes=to_int(minutes), hours=to_int(hours))
        self.scheduled_departure = dateutil.parser.parse(scheduled_dep, fuzzy=True) if scheduled_dep else None
        self.actual_departure = dateutil.parser.parse(actual_dep, fuzzy=True) if actual_dep else None
        self.arrival = dateutil.parser.parse(arrival, fuzzy=True) if arrival else None
        self._register_properties(['boat_name', 'sailing_time', 'scheduled_departure', 'actual_departure', 'arrival'])
        return

    def is_early(self):
        return (self.actual_departure or self.scheduled_departure) < self.scheduled_departure

    def is_late(self):
        return (self.actual_departure or self.scheduled_departure) > self.scheduled_departure

    def is_departed(self):
        return (self.actual_departure or self.scheduled_departure) <= datetime.datetime.now()

    def delta_from_schedule(self):
        actual_departure = self.actual_departure or self.scheduled_departure
        if self.is_early():
            return self.scheduled_departure - actual_departure
        else:
            return actual_departure - self.scheduled_departure