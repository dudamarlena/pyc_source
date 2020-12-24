# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/analytics/basemetric.py
# Compiled at: 2011-05-24 10:05:12


class BaseMetric(object):
    """
    Serves as a template for external apps' metrics. All
    functions specified in this object are compulsory.
    """
    uid = ''
    title = ''

    def calculate(self, start_datetime, end_datetime):
        """
        Must calculate the number of statistics between the two
        specified date/times. These date/times are passed from the
        calculator functions depending on the type of calculation
        being performed.

        Results must be returned for date >= start_datetime and
        date < end_datetime.
        """
        pass

    def get_earliest_timestamp(self):
        """
        Must return a date/time object indicating when the earliest
        data available for this metric occurred.
        """
        pass