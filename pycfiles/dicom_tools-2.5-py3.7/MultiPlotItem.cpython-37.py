# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/MultiPlotItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2062 bytes
"""
MultiPlotItem.py -  Graphics item used for displaying an array of PlotItems
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more infomation.
"""
from numpy import ndarray
from . import GraphicsLayout
from ..metaarray import *
__all__ = [
 'MultiPlotItem']

class MultiPlotItem(GraphicsLayout.GraphicsLayout):
    __doc__ = '\n    Automatically generates a grid of plots from a multi-dimensional array\n    '

    def __init__(self, *args, **kwds):
        (GraphicsLayout.GraphicsLayout.__init__)(self, *args, **kwds)
        self.plots = []

    def plot(self, data):
        if hasattr(data, 'implements') and data.implements('MetaArray'):
            if data.ndim != 2:
                raise Exception('MultiPlot currently only accepts 2D MetaArray.')
            ic = data.infoCopy()
            ax = 0
            for i in (0, 1):
                if 'cols' in ic[i]:
                    ax = i
                    break

            for i in range(data.shape[ax]):
                pi = self.addPlot()
                self.nextRow()
                sl = [slice(None)] * 2
                sl[ax] = i
                pi.plot(data[tuple(sl)])
                self.plots.append((pi, i, 0))
                info = ic[ax]['cols'][i]
                title = info.get('title', info.get('name', None))
                units = info.get('units', None)
                pi.setLabel('left', text=title, units=units)

            info = ic[(1 - ax)]
            title = info.get('title', info.get('name', None))
            units = info.get('units', None)
            pi.setLabel('bottom', text=title, units=units)
        else:
            raise Exception('Data type %s not (yet?) supported for MultiPlot.' % type(data))

    def close(self):
        for p in self.plots:
            p[0].close()

        self.plots = None
        self.clear()