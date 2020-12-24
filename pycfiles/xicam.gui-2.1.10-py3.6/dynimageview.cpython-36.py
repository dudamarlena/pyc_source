# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\gui\widgets\dynimageview.py
# Compiled at: 2018-07-06 18:13:03
# Size of source mod 2**32: 1289 bytes
from pyqtgraph import ImageView
import numpy as np

class DynImageView(ImageView):

    def __init__(self, *args, **kwargs):
        (super(DynImageView, self).__init__)(*args, **kwargs)
        self.setPredefinedGradient('viridis')
        self.getHistogramWidget().setMinimumWidth(10)
        self.view.invertY(False)
        self.sigTimeChangeFinished = self.timeLine.sigPositionChangeFinished

    def quickMinMax(self, data):
        """
        Estimate the min/max values of *data* by subsampling. MODIFIED TO USE THE 99TH PERCENTILE instead of max.
        """
        if data.size > 1000000.0:
            data = data[(len(data) // 2)]
        return (
         np.nanmin(data), np.nanpercentile(data, 99))

    def setImage(self, img, autoRange=True, autoLevels=True, levels=None, axes=None, xvals=None, pos=None, scale=None, transform=None, autoHistogramRange=True):
        super(DynImageView, self).setImage(img, autoRange, autoLevels, levels, axes, xvals, pos, scale, transform, autoHistogramRange)
        if len(img.shape) > 2:
            if img.shape[0] == 1:
                self.ui.roiPlot.hide()