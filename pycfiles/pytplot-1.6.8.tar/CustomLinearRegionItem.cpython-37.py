# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/CustomLinearRegionItem/CustomLinearRegionItem.py
# Compiled at: 2020-05-12 15:08:28
# Size of source mod 2**32: 725 bytes
import pyqtgraph as pg
from pyqtgraph import functions as fn

class CustomLinearRegionItem(pg.LinearRegionItem):
    __doc__ = "Inheriting the LinearRegionItem class because if someone hovers over a region of interest box,\n    I don't want it to have a different alpha value than when the mouse is not over the box."

    def setMouseHover(self, hover):
        if self.mouseHovering == hover:
            return
        else:
            self.mouseHovering = hover
            if hover:
                c = self.brush.color()
                c.setAlpha(c.alpha() * 1)
                self.currentBrush = fn.mkBrush(c)
            else:
                self.currentBrush = self.brush
        self.update()