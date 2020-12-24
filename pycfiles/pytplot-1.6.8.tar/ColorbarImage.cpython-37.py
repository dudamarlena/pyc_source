# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/CustomImage/ColorbarImage.py
# Compiled at: 2020-05-12 15:08:28
# Size of source mod 2**32: 3121 bytes
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np, collections
from pyqtgraph import functions as fn
from pyqtgraph import debug
import pyqtgraph.Point as Point
from collections.abc import Callable

class ColorbarImage(pg.ImageItem):
    __doc__ = '\n    For the most part, this class is exactly the same as pg.ImageItem.\n\n    This exist literally only because collections.Callable became collections.abc.Callable\n    and it was causing errors.\n    '

    def render(self):
        profile = debug.Profiler()
        if self.image is None or self.image.size == 0:
            return
        elif isinstance(self.lut, collections.abc.Callable):
            lut = self.lut(self.image)
        else:
            lut = self.lut
        if self.autoDownsample:
            o = self.mapToDevice(QtCore.QPointF(0, 0))
            x = self.mapToDevice(QtCore.QPointF(1, 0))
            y = self.mapToDevice(QtCore.QPointF(0, 1))
            w = Point(x - o).length()
            h = Point(y - o).length()
            if not w == 0:
                if h == 0:
                    self.qimage = None
                    return
                xds = max(1, int(1.0 / w))
                yds = max(1, int(1.0 / h))
                axes = [1, 0] if self.axisOrder == 'row-major' else [0, 1]
                image = fn.downsample((self.image), xds, axis=(axes[0]))
                image = fn.downsample(image, yds, axis=(axes[1]))
                self._lastDownsample = (xds, yds)
            else:
                image = self.image
        else:
            levels = self.levels
            if levels is not None:
                if levels.ndim == 1 and image.dtype in (np.ubyte, np.uint16):
                    if self._effectiveLut is None:
                        eflsize = 2 ** (image.itemsize * 8)
                        ind = np.arange(eflsize)
                        minlev, maxlev = levels
                        levdiff = maxlev - minlev
                        levdiff = 1 if levdiff == 0 else levdiff
                        if lut is None:
                            efflut = fn.rescaleData(ind, scale=(255.0 / levdiff), offset=minlev,
                              dtype=(np.ubyte))
                        else:
                            lutdtype = np.min_scalar_type(lut.shape[0] - 1)
                            efflut = fn.rescaleData(ind, scale=((lut.shape[0] - 1) / levdiff), offset=minlev,
                              dtype=lutdtype,
                              clip=(0, lut.shape[0] - 1))
                            efflut = lut[efflut]
                        self._effectiveLut = efflut
                    lut = self._effectiveLut
                    levels = None
        if self.axisOrder == 'col-major':
            image = image.transpose((1, 0, 2)[:image.ndim])
        argb, alpha = fn.makeARGB(image, lut=lut, levels=levels)
        self.qimage = fn.makeQImage(argb, alpha, transpose=False)