# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/insolation_meter.py
# Compiled at: 2014-10-18 19:15:55


class StaticInsolation(object):

    def __init__(self, surface_insolation=1, insolation_factor=0.1):
        super(StaticInsolation, self).__init__()
        self.surface_insolation = surface_insolation
        self.insolation_factor = insolation_factor

    def get_insolation(self, cell, step=0):
        depth = getattr(cell, 'depth', 0)
        return max(0, self.surface_insolation - depth * self.insolation_factor)


class DynamicInsolation(object):

    def __init__(self, seasons):
        super(DynamicInsolation, self).__init__()
        self.seasons = seasons

    def get_insolation(self, cell, step=0):
        depth = getattr(cell, 'depth', 0)
        step = step % sum(season[0] for season in self.seasons)
        if step == 0:
            season = self.seasons[(-1)]
        else:
            s = 0
            while step > self.seasons[s][0]:
                step -= self.seasons[s][0]
                s += 1

            season = self.seasons[s]
        return max(0, season[1] - depth * season[2])