# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/CustomViewBox/NoPaddingPlot.py
# Compiled at: 2020-04-24 00:12:01
# Size of source mod 2**32: 254 bytes
import pyqtgraph as pg

class NoPaddingPlot(pg.ViewBox):

    def suggestPadding(self, axis):
        l = self.width() if axis == 0 else self.height()
        if l > 0:
            padding = 0
        else:
            padding = 0
        return padding