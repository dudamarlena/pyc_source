# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanagercore/instant_time.py
# Compiled at: 2017-08-02 06:27:43
""" A representation of a datetime with a given granularity (day, week). """

class InstantTime:
    """ A representation of a datetime with a given granularity (day, week).
    """
    day, week = range(2)

    def __init__(self, datetime, granularity=None):
        """ Initialisation.

        :param datetime: the underlying datetime object
        :param granularity: granularity of the datetime, either
                            InstantTime.day or InstantTime.week.
        """
        self.datetime = datetime
        self.granularity = granularity or InstantTime.day

    @staticmethod
    def parse_grain(grain):
        """ Parse a string to a granularity, e.g. "Day" to InstantTime.day.

        :param grain: a string representing a granularity.
        """
        if not grain:
            return InstantTime.day
        if grain.lower() == 'week':
            return InstantTime.week
        return InstantTime.day