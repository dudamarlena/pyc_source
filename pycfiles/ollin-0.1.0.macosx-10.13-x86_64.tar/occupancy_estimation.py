# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/ollin/estimation/occupancy/occupancy_estimation.py
# Compiled at: 2018-07-30 01:23:46
from ..estimation import Estimate

class OccupancyEstimate(Estimate):
    __slots__ = [
     'occupancy', 'model', 'data', 'detectability']

    def __init__(self, occupancy, model, data, detectability=None):
        self.occupancy = occupancy
        self.model = model
        self.data = data
        self.detectability = detectability

    def __str__(self):
        msg = 'Occupancy estimation done with {} model.\n'
        msg += ('\tOccupancy: {}').format(self.occupancy)
        if self.detectability is not None:
            msg += ('\n\tDetectability: {}').format(self.detectability)
        return msg.format(self.model.name)