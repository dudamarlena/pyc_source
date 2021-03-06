# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/CustomImage/UpdatingImage.py
# Compiled at: 2020-04-24 00:12:01
# Size of source mod 2**32: 15642 bytes
import pyqtgraph as pg, numpy as np
from pyqtgraph.Qt import QtCore
from pyqtgraph import functions as fn
import pyqtgraph.Point as Point
from pyqtgraph import debug
from collections.abc import Callable
from pytplot import tplot_opt_glob
import pandas as pd

class UpdatingImage(pg.ImageItem):
    __doc__ = '\n    This is the class used to plot images of spectrogram data.\n\n    It automatically updates to higher and higher resolutions when you zoom in, thus the name\n    "updating image".\n\n    '
    _MAX_IMAGE_WIDTH = 10000
    _MAX_IMAGE_HEIGHT = 2000

    def __init__(self, data, spec_bins, ascending_descending, ytype, ztype, lut, ymin, ymax, zmin, zmax):
        pg.ImageItem.__init__(self)
        if ztype == 'log':
            data[data <= 0] = np.NaN
            self.data = np.log10(data)
            self.zmin = np.log10(zmin)
            self.zmax = np.log10(zmax)
        else:
            self.data = data
            self.zmin = zmin
            self.zmax = zmax
        self.ytype = ytype
        self.lut = lut
        self.bin_sizes = spec_bins
        self.bins_inc = ascending_descending
        self.w = 100
        self.h = 100
        self.x = self.data.index.tolist()
        self.xmin = np.nanmin(self.x)
        self.xmax = np.nanmax(self.x)
        if len(spec_bins) != 1:
            xp = np.linspace(self.xmin, self.xmax, 1000)
            closest_xs = np.searchsorted(self.x, xp)
            minbin = ymin
            maxbin = ymax
            if ytype == 'log':
                yp = np.logspace(np.log10(minbin), np.log10(maxbin), 100)
            else:
                yp = np.linspace(minbin, maxbin, 100)
            data_reformatted = []
            y_sort = np.argsort(self.bin_sizes.iloc[0].tolist())
            prev_bins = self.bin_sizes.iloc[0]
            prev_closest_ys = np.searchsorted((self.bin_sizes.iloc[0]), yp, sorter=y_sort)
            prev_closest_ys[prev_closest_ys > len(self.bin_sizes.iloc[0]) - 1] = len(self.bin_sizes.iloc[0]) - 1
            for i in closest_xs:
                if (self.bin_sizes.iloc[i] == prev_bins).all():
                    closest_ys = prev_closest_ys
                else:
                    prev_bins = self.bin_sizes.iloc[i]
                    closest_ys = np.searchsorted((self.bin_sizes.iloc[i]), yp, sorter=y_sort)
                    closest_ys[closest_ys > len(self.bin_sizes.iloc[i]) - 1] = len(self.bin_sizes.iloc[i]) - 1
                    prev_closest_ys = closest_ys
                temp_data = self.data.iloc[i][closest_ys].values
                try:
                    temp_data[yp < np.nanmin(self.bin_sizes.iloc[i])] = np.NaN
                    temp_data[yp > np.nanmax(self.bin_sizes.iloc[i])] = np.NaN
                except RuntimeWarning:
                    pass

                data_reformatted.append(temp_data)

            data_reformatted = pd.DataFrame(data_reformatted)
            self.x = xp
            self.y = np.linspace(np.log10(minbin), np.log10(maxbin), 100)
            self.data = data_reformatted
        else:
            if ytype == 'log':
                self.y = np.log10(self.bin_sizes.iloc[0])
            else:
                self.y = self.bin_sizes.iloc[0]
        if ytype == 'log':
            self.ymin = np.log10(ymin)
            self.ymax = np.log10(ymax)
        else:
            self.ymin = ymin
            self.ymax = ymax
        self.picturenotgened = True
        self.generatePicture()

    def generatePicture(self, pixel_size=None):
        if pixel_size is None:
            width_in_pixels = tplot_opt_glob['window_size'][0]
            height_in_pixels = tplot_opt_glob['window_size'][1]
            width_in_plot_coords = tplot_opt_glob['window_size'][0]
            height_in_plot_coords = tplot_opt_glob['window_size'][1]
        else:
            width_in_pixels = pixel_size.width()
            height_in_pixels = pixel_size.height()
            width_in_plot_coords = self.getViewBox().viewRect().width()
            height_in_plot_coords = self.getViewBox().viewRect().height()
        image_width_in_plot_coords = self.xmax - self.xmin
        image_height_in_plot_coords = self.ymax - self.ymin
        image_width_in_pixels = int(image_width_in_plot_coords / width_in_plot_coords * width_in_pixels)
        image_height_in_pixels = int(image_height_in_plot_coords / height_in_plot_coords * height_in_pixels)
        if image_width_in_pixels > self._MAX_IMAGE_WIDTH:
            image_width_in_pixels = self._MAX_IMAGE_WIDTH
        if image_height_in_pixels > self._MAX_IMAGE_HEIGHT:
            image_height_in_pixels = self._MAX_IMAGE_HEIGHT
        if self.w != image_width_in_pixels or self.h != image_height_in_pixels:
            self.w = image_width_in_pixels
            self.h = image_height_in_pixels
            if self.w == 0:
                self.w = 1
            if self.h == 0:
                self.h = 1
            data = np.zeros((self.h, self.w))
            xp = np.linspace(self.xmin, self.xmax, self.w)
            yp = np.linspace(self.ymin, self.ymax, self.h)
            closest_xs = np.searchsorted(self.x, xp)
            y_sort = np.argsort(self.y.tolist())
            closest_ys = np.searchsorted((self.y), yp, sorter=y_sort)
            closest_ys[closest_ys == len(self.y)] = len(self.y) - 1
            if not self.bins_inc:
                closest_ys = np.flipud(closest_ys)
            data = self.data.iloc[closest_xs][closest_ys].values
            self.setImage((data.T), levels=(self.zmin, self.zmax))
            self.setLookupTable((self.lut), update=False)
            self.setRect(QtCore.QRectF(self.xmin, self.ymin, self.xmax - self.xmin, self.ymax - self.ymin))
            return

    def paint(self, p, *args):
        """
        I have no idea why, but we need to generate the picture after painting otherwise 
        it draws incorrectly.  
        """
        if self.picturenotgened:
            self.generatePicture(self.getBoundingParents()[0].rect())
            self.picturenotgened = False
        (pg.ImageItem.paint)(self, p, *args)
        self.generatePicture(self.getBoundingParents()[0].rect())

    def render(self):
        profile = debug.Profiler()
        if self.image is None or self.image.size == 0:
            return
        elif isinstance(self.lut, Callable):
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
        argb, alpha = makeARGBwithNaNs(image, lut=lut, levels=levels)
        self.qimage = fn.makeQImage(argb, alpha, transpose=False)

    def setImage(self, image=None, autoLevels=None, **kargs):
        """
        Same this as ImageItem.setImage, but we don't update the drawing
        """
        profile = debug.Profiler()
        gotNewData = False
        if image is None:
            if self.image is None:
                return
        else:
            gotNewData = True
            shapeChanged = self.image is None or image.shape != self.image.shape
            image = image.view(np.ndarray)
        if not self.image is None:
            if image.dtype != self.image.dtype:
                self._effectiveLut = None
            self.image = image
            if self.image.shape[0] > 32767 or self.image.shape[1] > 32767:
                if 'autoDownsample' not in kargs:
                    kargs['autoDownsample'] = True
            if shapeChanged:
                self.prepareGeometryChange()
                self.informViewBoundsChanged()
        else:
            profile()
            if autoLevels is None:
                if 'levels' in kargs:
                    autoLevels = False
                else:
                    autoLevels = True
        if autoLevels:
            img = self.image
            while img.size > 65536:
                img = img[::2, ::2]

            mn, mx = img.min(), img.max()
            if mn == mx:
                mn = 0
                mx = 255
            kargs['levels'] = [
             mn, mx]
        profile()
        (self.setOpts)(update=False, **kargs)
        profile()
        self.qimage = None
        self.update()
        profile()
        if gotNewData:
            self.sigImageChanged.emit()


def makeARGBwithNaNs(data, lut=None, levels=None, scale=None, useRGBA=False):
    """ 
    This is the same as pyqtgraph.makeARGB, except that all NaN's in the data are set to transparent pixels
    """
    nanlocations = np.isnan(data)
    profile = debug.Profiler()
    if data.ndim not in (2, 3):
        raise TypeError('data must be 2D or 3D')
    if data.ndim == 3:
        if data.shape[2] > 4:
            raise TypeError('data.shape[2] must be <= 4')
    if lut is not None:
        if not isinstance(lut, np.ndarray):
            lut = np.array(lut)
        elif levels is None:
            if data.dtype.kind == 'u':
                levels = np.array([0, 2 ** (data.itemsize * 8) - 1])
            else:
                if data.dtype.kind == 'i':
                    s = 2 ** (data.itemsize * 8 - 1)
                    levels = np.array([-s, s - 1])
                else:
                    if data.dtype.kind == 'b':
                        levels = np.array([0, 1])
                    else:
                        raise Exception('levels argument is required for float input types')
        if not isinstance(levels, np.ndarray):
            levels = np.array(levels)
        if levels.ndim == 1:
            if levels.shape[0] != 2:
                raise Exception('levels argument must have length 2')
    elif levels.ndim == 2:
        if lut is not None:
            if lut.ndim > 1:
                raise Exception('Cannot make ARGB data when both levels and lut have ndim > 2')
            elif levels.shape != (data.shape[(-1)], 2):
                raise Exception('levels must have shape (data.shape[-1], 2)')
            else:
                raise Exception('levels argument must be 1D or 2D (got shape=%s).' % repr(levels.shape))
        else:
            profile()
            if scale is None:
                if lut is not None:
                    scale = lut.shape[0] - 1
                else:
                    scale = 255.0
            if lut is None:
                dtype = np.ubyte
            else:
                dtype = np.min_scalar_type(lut.shape[0] - 1)
        if levels is not None:
            if isinstance(levels, np.ndarray) and levels.ndim == 2:
                if levels.shape[0] != data.shape[(-1)]:
                    raise Exception('When rescaling multi-channel data, there must be the same number of levels as channels (data.shape[-1] == levels.shape[0])')
                newData = np.empty((data.shape), dtype=int)
                for i in range(data.shape[(-1)]):
                    minVal, maxVal = levels[i]
                    if minVal == maxVal:
                        maxVal += 1e-16
                    newData[(..., i)] = fn.rescaleData((data[(..., i)]), (scale / (maxVal - minVal)), minVal, dtype=dtype)

                data = newData
    else:
        minVal, maxVal = levels
    if minVal != 0 or maxVal != scale:
        if minVal == maxVal:
            maxVal += 1e-16
        data = fn.rescaleData(data, (scale / (maxVal - minVal)), minVal, dtype=dtype)
    profile()
    if lut is not None:
        data = fn.applyLookupTable(data, lut)
    else:
        if data.dtype is not np.ubyte:
            data = np.clip(data, 0, 255).astype(np.ubyte)
        else:
            data[nanlocations] = [
             0, 0, 0, 0]
            profile()
            imgData = np.empty((data.shape[:2] + (4, )), dtype=(np.ubyte))
            profile()
            if useRGBA:
                order = [
                 0, 1, 2, 3]
            else:
                order = [
                 2, 1, 0, 3]
            if data.ndim == 2:
                for i in range(3):
                    imgData[(..., i)] = data

            else:
                if data.shape[2] == 1:
                    for i in range(3):
                        imgData[(..., i)] = data[(Ellipsis, 0)]

                else:
                    for i in range(0, data.shape[2]):
                        imgData[(..., i)] = data[(..., order[i])]

            profile()
            if data.ndim == 2 or data.shape[2] == 3:
                alpha = False
                imgData[(Ellipsis, 3)] = 255
            else:
                alpha = True
        profile()
        return (imgData, alpha)