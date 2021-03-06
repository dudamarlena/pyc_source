# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/CustomAxis/NonLinearAxis.py
# Compiled at: 2020-04-04 16:23:02
# Size of source mod 2**32: 1004 bytes
import pyqtgraph as pg

class NonLinearAxis(pg.AxisItem):

    def __init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True, mapping_function=None):
        pg.AxisItem.__init__(self, orientation=orientation, pen=pen, linkView=linkView, parent=parent, maxTickLength=maxTickLength, showValues=showValues)
        self.f = mapping_function
        self.num_ticks = 4

    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            try:
                strns.append(str(int(self.f(x))))
            except ValueError:
                strns.append('')

        return strns

    def tickValues(self, minVal, maxVal, size):
        minVal, maxVal = sorted((minVal, maxVal))
        minVal *= self.scale
        maxVal *= self.scale
        ticks = []
        xrange = maxVal - minVal
        for i in range(0, self.num_ticks + 1):
            ticks.append(minVal + i * xrange / self.num_ticks)

        return [
         (
          1.0, ticks)]