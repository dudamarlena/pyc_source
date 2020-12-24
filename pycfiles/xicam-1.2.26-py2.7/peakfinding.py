# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\peakfinding.py
# Compiled at: 2018-08-27 17:21:06
import numpy as np
from scipy import signal
from scipy.ndimage import filters
from xicam import debugtools
import pyqtgraph as pg
from PySide import QtCore
wavelet = signal.ricker
widths = np.arange(1, 20)
max_distances = widths / 8.0
gap_thresh = 4
min_length = 3
min_snr = 2
noise_perc = 10
h = 3
truncationlow = 10
truncationhigh = 50

@debugtools.timeit
def findpeaks(x, y):
    peaks = signal.find_peaks_cwt(y, widths, wavelet, max_distances, gap_thresh, min_length, min_snr, noise_perc)
    peaks = peaks[1:]
    return list(np.array(np.vstack([x[peaks], y[peaks], peaks])))


class peaktooltip:

    def __init__(self, x, y, widget):
        self.q, self.I, self.width, self.index = findpeaks(x, y)
        self.scatterPoints = pg.PlotDataItem(self.q, self.I, size=10, pen=pg.mkPen(None), symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120), symbol='o')
        self.display_text = pg.TextItem(text='', color=(176, 23, 31), anchor=(0, 1))
        self.display_text.hide()
        widget.addItem(self.scatterPoints)
        widget.addItem(self.display_text)
        self.scatterPoints.scene().sigMouseMoved.connect(self.onMove)
        return

    def onMove(self, pixelpos):
        itempos = self.scatterPoints.mapFromScene(pixelpos)
        itemx = itempos.x()
        itemy = itempos.y()
        pixeldelta = 7
        delta = self.scatterPoints.mapFromScene(QtCore.QPointF(pixeldelta + pixelpos.x(), pixeldelta + pixelpos.y()))
        deltax = delta.x() - itemx
        deltay = -(delta.y() - itemy)
        p1 = [ point for point in zip(self.q, self.I) if itemx - deltax < point[0] and point[0] < itemx + deltax and itemy - deltay < point[1] and point[1] < itemy + deltay
             ]
        if len(p1) != 0:
            self.display_text.setText('q=%f\nI=%f' % (p1[0][0], p1[0][1]))
            self.display_text.setPos(*p1[0])
            self.display_text.show()
        else:
            self.display_text.hide()