# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/CustomAxis/BlankAxis.py
# Compiled at: 2020-04-24 00:12:01
# Size of source mod 2**32: 698 bytes
import pyqtgraph as pg

class BlankAxis(pg.AxisItem):

    def __init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        pg.AxisItem.__init__(self, orientation=orientation, pen=pen, linkView=linkView, parent=parent, maxTickLength=maxTickLength, showValues=showValues)

    def tickStrings(self, values, scale, spacing):
        strns = []
        for _ in values:
            try:
                strns.append('')
            except ValueError:
                strns.append('')

        return strns