# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_metadata/filter.py
# Compiled at: 2010-01-20 18:10:50
from hachoir_metadata.timezone import UTC
from datetime import date, datetime
MIN_YEAR = 1850
MAX_YEAR = 2030

class Filter:
    __module__ = __name__

    def __init__(self, valid_types, min=None, max=None):
        self.types = valid_types
        self.min = min
        self.max = max

    def __call__(self, value):
        if not isinstance(value, self.types):
            return True
        if self.min is not None and value < self.min:
            return False
        if self.max is not None and self.max < value:
            return False
        return True


class NumberFilter(Filter):
    __module__ = __name__

    def __init__(self, min=None, max=None):
        Filter.__init__(self, (int, long, float), min, max)


class DatetimeFilter(Filter):
    __module__ = __name__

    def __init__(self, min=None, max=None):
        Filter.__init__(self, (date, datetime), datetime(MIN_YEAR, 1, 1), datetime(MAX_YEAR, 12, 31))
        self.min_date = date(MIN_YEAR, 1, 1)
        self.max_date = date(MAX_YEAR, 12, 31)
        self.min_tz = datetime(MIN_YEAR, 1, 1, tzinfo=UTC)
        self.max_tz = datetime(MAX_YEAR, 12, 31, tzinfo=UTC)

    def __call__(self, value):
        """
        Use different min/max values depending on value type
        (datetime with timezone, datetime or date).
        """
        if not isinstance(value, self.types):
            return True
        if hasattr(value, 'tzinfo') and value.tzinfo:
            return self.min_tz <= value <= self.max_tz
        elif isinstance(value, datetime):
            return self.min <= value <= self.max
        else:
            return self.min_date <= value <= self.max_date


DATETIME_FILTER = DatetimeFilter()