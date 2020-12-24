# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/gazehound/viewing.py
# Compiled at: 2010-07-19 17:14:05
import copy
from gazehound import timeline, gazepoint

class Combiner(object):
    """Combines timelines of eventss with pointpath data"""

    def __init__(self, timeline=None, pointpath=None):
        self.timeline = timeline
        self.pointpath = pointpath

    def viewings(self):
        t2 = copy.copy(self.timeline)
        for pres in t2:
            points = [ p for p in self.pointpath if p.time_midpoint() >= pres.start if p.time_midpoint() < pres.end
                     ]
            pres.pointpath = gazepoint.PointPath(points)

        return timeline.Timeline(t2)