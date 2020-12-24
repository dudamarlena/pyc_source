# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/classes/observation.py
# Compiled at: 2018-07-03 20:51:00
# Size of source mod 2**32: 3745 bytes
import numpy as np

class TimeWindow(object):
    __doc__ = '\n    This class defines a Time Window and is the lowest level time entity for\n    spiops. The time window is generated with a start and finish times and it\n    can also indicate a current instant.\n    '

    def __init__(self, start, finish, current=False, resolution=False, abcorr='NONE', format='UTC'):
        """
        This method creates a new Time Window.

        :param start: Start time of the time window
        :type start: Union[str, float]
        :param finish: Finish time of the time window
        :type finish: Union[str, float]
        :param current: Selected time within the time window (used for computations that might require a current time)
        :type current: Union[str, float]
        :param resolution: Resolution of the time window in seconds
        :type resolution: float
        :param abcorr: Aberration Correction to be used for the Time Window
        :type abcorr: str
        :param format: Calendar format in which we want to see times ('UTC' or 'CAL')
        :type format: str
        """
        self.isInit = True
        self.res = resolution
        self.format = format
        self.abcorr = abcorr
        self.start = start
        self.finish = finish
        if not current:
            self.current = start
        else:
            self.current = current
        self.isInit = False
        self._TimeWindow__buildTimeSet()

    def __buildTimeSet(self):
        """
        Internal method to generate the time set of the time window.
        """
        if self.isInit:
            return
        if self.start > self.finish:
            return
        if self.start == self.finish:
            self.window = [
             self.start]
            return
        if not self.res or self.res >= self.finish - self.start:
            print('No resolution provided or resolution is bigger than the time interval. Setting to default')
            self.res = (self.finish - self.start) / 10.0
        self.window = np.arange(self.start, self.finish, self.res)

    def getTime(self, item, format=False):
        """

        :param item: Time to get: 'start', 'finish', 'current' or 'window'
        :type item: str
        :param format: Format to get the time: 'UTC' or 'CAL'
        :type format: str
        :return: Requested time in requested format
        :rtype: str
        :raise: If an invalid item is provided
        """
        import spiops.utils.time as zztime
        if format:
            format = format
        else:
            format = self.format
        if item in ('start', 'finish', 'current', 'window'):
            return zztime.et2cal(object.__getattribute__(self, item), format)
        raise ValueError('invalid time item: {}'.format(item))

    def __getattribute__(self, item):
        if item in ('start', 'finish', 'current', 'window'):
            return object.__getattribute__(self, item)
        else:
            return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        import spiops.utils.time as zztime
        if key in ('start', 'finish', 'current'):
            if isinstance(value, str):
                value = zztime.cal2et(value, format=self.format)
                super(TimeWindow, self).__setattr__(key, value)
                if key in ('start', 'finish'):
                    self._TimeWindow__buildTimeSet()
        else:
            super(TimeWindow, self).__setattr__(key, value)