# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/core/track/automation_item.py
# Compiled at: 2019-02-21 08:10:36
# Size of source mod 2**32: 3231 bytes
from reapy import reascript_api as RPR
from reapy.core import ReapyObject

class AutomationItem(ReapyObject):
    _class_name = 'AutomationItem'

    def __init__(self, envelope=None, index=0, envelope_id=None):
        if envelope is not None:
            envelope_id = envelope.id
        self.envelope_id = envelope_id
        self.index = index

    @property
    def _kwargs(self):
        return {'index': self.index, 'envelope_id': self.envelope_id}

    def delete_points_in_range(self, start, end):
        """
        Delete points between `start` and `end`.

        Parameters
        ----------
        start : float
            Range start in seconds.
        end : float
            Range end in seconds.
        """
        RPR.DeleteEnvelopePointRangeEx(self.envelope_id, self.index, start, end)

    @property
    def length(self):
        """
        Return item length in seconds.

        Returns
        -------
        length : float
            Item length in seconds.
        """
        length = RPR.GetSetAutomationItemInfo(self.envelope_id, self.index, 'D_LENGTH', 0, False)
        return length

    @length.setter
    def length(self, length):
        """
        Set item length.

        Parameters
        ----------
        length : float
            New item length in seconds.
        """
        success = RPR.GetSetAutomationItemInfo(self.envelope_id, self.index, 'D_LENGTH', length, True)

    @property
    def n_points(self):
        """
        Return number of automation points in item.

        Returns
        -------
        n_points : int
            Number of automation points in item.
        """
        n_points = RPR.CountEnvelopePointsEx(self.envelope_id, self.index)
        return n_points

    @property
    def pool(self):
        """
        Return item pool.

        Returns
        -------
        pool : int
            Item pool.
        """
        pool = RPR.GetSetAutomationItemInfo(self.envelope_id, self.index, 'D_POOL', 0, False)
        return pool

    @pool.setter
    def pool(self, pool):
        """
        Set item pool.

        Parameters
        ----------
        pool : int
            New item pool.
        """
        success = RPR.GetSetAutomationItemInfo(self.envelope_id, self.index, 'D_POOL', pool, True)

    @property
    def position(self):
        """
        Return item position in seconds.

        Returns
        -------
        position : float
            Item position in seconds.
        """
        position = RPR.GetSetAutomationItemInfo(self.envelope_id, self.index, 'D_POSITION', 0, False)
        return position

    @position.setter
    def position(self, position):
        """
        Set item position.

        Parameters
        ----------
        position : float
            New item position in seconds.
        """
        success = RPR.GetSetAutomationItemInfo(self.envelope_id, self.index, 'D_POSITION', position, True)