# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/visualise.py
# Compiled at: 2014-03-13 02:41:33
"""
@author: James McInerney
"""
from matplotlib.pyplot import *
from numpy import *
from vb_ihmm.testing.util import create_cov_ellipse
from util import inv0
from scipy import stats
import os
from vb_ihmm.model.util import findLim

class Anim(object):

    def __init__(self, sensor, fig, axLabels=None, plotLim=None, ellipseColor='r', dataSelect=0, savePath=None, mu_grnd=None):
        self._sensor = sensor
        self._fig = fig
        self._savePath = savePath
        self._mu_grnd = mu_grnd
        self._titleText = None
        self._sctX = None
        self._cumulativeX = None
        self._dataSelect = dataSelect
        self._N = 0
        self._plotLim = plotLim
        self._axLabels = axLabels
        self._graphMargin = 0.1
        return

    def update(self, itr, showThreshold):
        pl = self._plotLim
        if pl is None:
            mn, mx = findLim(self._cumulativeX, graphMargin=self._graphMargin)
            pl = zeros((2, 2))
            pl[:, 0], pl[:, 1] = mn, mx
        self._ax_spatial.set_xlim(pl[(0, 0)], pl[(0, 1)])
        self._ax_spatial.set_ylim(pl[(1, 0)], pl[(1, 1)])
        if self._axLabels is not None:
            self._ax_spatial.set_xlabel(self._axLabels[0])
            self._ax_spatial.set_ylabel(self._axLabels[1])
        if self._titleText is not None:
            self._ax_spatial.set_title(self._titleText)
        self._fig.canvas.draw()
        if self._savePath is not None:
            self._fig.savefig(self._savePath % {'itr': itr})
        return

    def setTitleText(self, txt):
        self._titleText = txt


class Anim2D(Anim):

    def __init__(self, sensor, plotLim=None, ellipseColor='r', dataSelect=arange(2), savePath=None, mu_grnd=None):
        ion()
        fig = figure(figsize=(10, 10))
        self._ax_spatial = fig.add_subplot(1, 1, 1)
        self._circs = []
        self._ellipseColor = ellipseColor
        self._newPlot = 1
        Anim.__init__(self, sensor, fig, plotLim=plotLim, dataSelect=dataSelect, savePath=savePath, mu_grnd=mu_grnd)

    def update(self, itr, showThreshold):
        sensor = self._sensor
        X = sensor.X()[:, self._dataSelect]
        mu_grnd = self._mu_grnd
        currentN, _ = shape(X)
        if self._sctX is None:
            self._sctX = self._ax_spatial.scatter(X[:, 0], X[:, 1], marker='x', color='g')
        else:
            self._sctX.set_offsets(self._cumulativeX)
        self._N = currentN
        ks_all = sensor._NK
        K = len(ks_all)
        ks, = where(ks_all > showThreshold)
        if self._newPlot:
            self._sctZ = self._ax_spatial.scatter(sensor._m[:, 0], sensor._m[:, 1], color='r')
            if mu_grnd is not None:
                K_grnd, _ = shape(mu_grnd)
                for k in range(K_grnd):
                    print 'plotting', mu_grnd[(k, 0)], mu_grnd[(k, 1)]
                    self._ax_spatial.scatter(mu_grnd[(k, 0)], mu_grnd[(k, 1)], color='k', marker='d', s=50)

            self._newPlot = 0
        else:
            self._updateCovariances(showThreshold, sensor)
            hiddenOffsets = 99999 * ones((K, len(self._dataSelect)))
            hiddenOffsets[ks, :] = sensor._m[ks, :][:, self._dataSelect]
            self._sctZ.set_offsets(hiddenOffsets)
        Anim.update(self, itr, showThreshold)
        return

    def _updateCovariances(self, showThreshold, sensor):
        ks_all = sensor._NK
        for circ in self._circs:
            circ.remove()

        self._circs = []
        ks, = where(ks_all > showThreshold)
        for k in ks:
            sensor._m[k, :]
            W = sensor.expC()
            C = W[k][self._dataSelect, :][:, self._dataSelect]
            circ = create_cov_ellipse(C, sensor._m[(k, self._dataSelect)], color=self._ellipseColor, alpha=0.1)
            self._circs.append(circ)
            self._ax_spatial.add_artist(circ)


class AnimReported(Anim2D):

    def _updateCovariances(self, showThreshold, sensor):
        for circ in self._circs:
            circ.remove()

        self._circs = []
        X = sensor._X
        N, XDim = shape(X)
        C = sensor.expC()
        assert shape(C) == (N, XDim, XDim)
        for n in range(N):
            D = C[n, :, :][self._dataSelect, :][:, self._dataSelect]
            circ = create_cov_ellipse(D, X[(n, self._dataSelect)], color=self._ellipseColor, alpha=0.1)
            self._circs.append(circ)
            self._ax_spatial.add_artist(circ)


class Anim1D(Anim):

    def __init__(self, sensor, plotLim=None, ellipseColor='r', dataSelect=0, savePath=None, mu_grnd=None):
        self._sensor = sensor
        ion()
        fig = figure(figsize=(10, 10))
        self._ax_spatial = fig.add_subplot(1, 1, 1)
        self._lines = []
        self._ellipseColor = ellipseColor
        self._savePath = savePath
        self._mu_grnd = mu_grnd
        self._newPlot = 1
        self._titleText = None
        self._sctX = None
        self._cumulativeX = None
        self._N = 0
        self._dataSelect = dataSelect
        Anim.__init__(self, sensor, fig, plotLim=plotLim, dataSelect=dataSelect, savePath=savePath, mu_grnd=mu_grnd)
        return

    def update(self, itr, showThreshold):
        sensor = self._sensor
        X = sensor.X()[:, self._dataSelect]
        mu_grnd = self._mu_grnd
        ds = self._dataSelect
        currentN, = shape(X)
        ks_all = sensor._NK
        K = len(ks_all)
        ks, = where(ks_all > showThreshold)
        if self._sctX is None:
            self._sctX = self._ax_spatial.scatter(X, zeros(currentN), marker='x', color='g')
        self._N = currentN
        xs = arange(0, 24, 0.01)
        if self._newPlot:
            self._sctZ = self._ax_spatial.scatter(sensor._m[:, ds], zeros(K), color='r')
            if mu_grnd is not None:
                K_grnd, _ = shape(mu_grnd)
                for k in range(K_grnd):
                    self._ax_spatial.scatter(mu_grnd[(k, ds)], 0, color='k', marker='d', s=50)

            self._newPlot = 0
            W = sensor.expC()
            for k in range(K):
                C = W[k][self._dataSelect]
                ys = stats.norm.pdf(xs, sensor._m[(k, ds)], C)
                p, = self._ax_spatial.plot(xs, ys, color='r')
                self._lines.append(p)

        else:
            for k in range(K):
                sensor._m[k, :]
                W = sensor.expC()
                C = sqrt(W[k][self._dataSelect])
                if k in ks:
                    ys = stats.norm.pdf(xs, sensor._m[(k, ds)], C)
                else:
                    ys = inf + zeros(len(xs))
                self._lines[k].set_ydata(ys)

            mus = zeros((K, 2))
            mus[:, 0] = sensor._m[:, ds]
            self._sctZ.set_offsets(mus)
        Anim.update(self, itr, showThreshold)
        return


class AnimLine(Anim):

    def __init__(self, data, plotLim=None, savePath=None, lineColor='b', scatY=None, plotVert=None, labels=['', '', '']):
        self._data = data
        self._lineColor = lineColor
        ion()
        fig = figure(figsize=(10, 10))
        self._ax_spatial = fig.add_subplot(1, 1, 1)
        self._lines = []
        self._savePath = savePath
        self._newPlot = 1
        self._titleText = None
        self._N = 0
        self._scatY = scatY
        self._plotVert = plotVert
        self._labels = labels
        Anim.__init__(self, None, fig, plotLim=plotLim, savePath=savePath)
        return

    def update(self, itr, showThreshold):
        xs, ys = self._data()[:, 0], self._data()[:, 1]
        if self._scatY:
            scatY = self._scatY()
        if self._newPlot:
            if self._scatY is not None:
                self._scatAx = self._ax_spatial.scatter(scatY[:, 0], scatY[:, 1], marker='x', color='r', label=self._labels[2])
            if self._plotVert is not None:
                doneLbl = 0
                for xpoint in self._plotVert:
                    if xpoint > 0:
                        if not doneLbl:
                            self._ax_spatial.plot([xpoint, xpoint], [0, 1], color='gray', label=self._labels[1])
                            doneLbl = 1
                        else:
                            self._ax_spatial.plot([xpoint, xpoint], [0, 1], color='gray')

            self._newPlot = 0
            p, = self._ax_spatial.plot(xs, ys, color=self._lineColor, label=self._labels[0])
            self._lines.append(p)
        else:
            self._lines[0].set_ydata(ys)
            if self._scatY:
                self._scatAx.set_offsets(scatY)
        self._cumulativeX = array([[xs.min(), ys.min()], [xs.max(), ys.max()]])
        if any([ l != '' for l in self._labels ]):
            self._ax_spatial.legend()
        Anim.update(self, itr, showThreshold)
        return


class AnimScatter(Anim):

    def __init__(self, data, targetArg, axLabels=None, plotLim=None, savePath=None, lineColor='b', scatY=None, plotVert=None, labels=['', '', '']):
        self._data = data
        self._targetArg = targetArg
        self._lineColor = lineColor
        ion()
        fig = figure(figsize=(10, 10))
        self._ax_spatial = fig.add_subplot(1, 1, 1)
        self._ax_spatial.minorticks_on()
        self._lines = []
        self._savePath = savePath
        self._newPlot = 1
        self._titleText = None
        self._N = 0
        self._scatY = scatY
        self._plotVert = plotVert
        self._labels = labels
        Anim.__init__(self, None, fig, plotLim=plotLim, savePath=savePath, axLabels=axLabels)
        return

    def update(self, itr, showThreshold):
        xs, ys = self._data(self._targetArg)[:, 0], self._data(self._targetArg)[:, 1]
        if self._scatY:
            scatY = self._scatY()
        if self._newPlot:
            if self._scatY is not None:
                self._scatAx = self._ax_spatial.scatter(scatY[:, 0], scatY[:, 1], marker='x', color='r', label=self._labels[2])
            if self._plotVert is not None:
                doneLbl = 0
                for xpoint in self._plotVert:
                    if xpoint > 0:
                        if not doneLbl:
                            self._ax_spatial.plot([xpoint, xpoint], [0, 1], color='g', label=self._labels[1], marker='x')
                            doneLbl = 1
                        else:
                            self._ax_spatial.plot([xpoint, xpoint], [0, 1], color='gray')

            self._newPlot = 0
            print 'xs', xs
            print 'ys', ys
            p = self._ax_spatial.scatter(xs, ys, color=self._lineColor, marker='x', label=self._labels[0])
            self._lines.append(p)
        else:
            self._lines[0].set_offsets(vstack((xs, ys)).T)
            if self._scatY:
                self._scatAx.set_offsets(scatY)
        self._cumulativeX = array([[xs.min(), ys.min()], [xs.max(), ys.max()]])
        if any([ l != '' for l in self._labels ]):
            self._ax_spatial.legend()
        Anim.update(self, itr, showThreshold)
        return


class AnimBlocks(Anim):

    def __init__(self, sensor, slice=None, plotLim=None, savePath=None):
        ion()
        fig = figure(figsize=(10, 10))
        self._fig = fig
        self._ax_spatial = fig.add_subplot(1, 1, 1)
        self._newPlot = 1
        self._slice = slice
        self._rects = []
        self._graphMargin = 0.0
        Anim.__init__(self, sensor, fig, plotLim=plotLim, dataSelect=None, savePath=savePath, mu_grnd=None)
        return

    def update(self, itr, showThreshold):
        slice = self._slice
        if slice is not None:
            exp_a = self._sensor.expA()[:, :, slice]
        else:
            exp_a = self._sensor.expA()[:, :]
        N, M = shape(exp_a)
        self._cumulativeX = array([[0, 0], [N - 1, M - 1]])
        if self._newPlot:
            for j in range(N):
                self._ax_spatial.plot([j, j], [0, N], color='gray', alpha=0.3)

            for i in range(M):
                self._ax_spatial.plot([0, M], [i, i], color='gray', alpha=0.3)

            ax = self._ax_spatial
            for i in range(N):
                self._rects.append([])
                for j in range(M):
                    rect = Rectangle((i, j), 1, 1, alpha=0.0)
                    ax.add_patch(rect)
                    self._rects[(-1)].append(rect)

            self._newPlot = 0
        else:
            self._fig.gca().invert_yaxis()
            K, ks = self._sensor.sigComponents(thres=showThreshold)
            for i in range(N):
                for j in range(M):
                    if j in ks:
                        self._rects[j][i].set_alpha(exp_a[(i, j)])
                    else:
                        self._rects[j][i].set_alpha(0.0)

        Anim.update(self, itr, showThreshold)
        return


class AnimComposite(Anim):

    def __init__(self, animations, numRows=2, savePath=None, montageLoc='/opt/local/bin/montage'):
        self._animations = animations
        self._numRows = numRows
        self._savePath = savePath
        self._montageLoc = montageLoc

    def update(self, itr, showThreshold):
        [ a.update(itr, showThreshold) for a in self._animations ]
        if self._savePath is not None:
            plotNames = [ a._savePath % {'itr': itr} for a in self._animations if a._savePath is not None ]
            print 'plotNames', plotNames
            print 'composite path', self._savePath % {'itr': itr}
            fileStr = (' ').join(plotNames)
            numRows = self._numRows
            os.system('%s -mode concatenate -tile x%i %s %s' % (self._montageLoc, numRows, fileStr, self._savePath % {'itr': itr}))
            [ os.system('rm %s' % p) for p in plotNames ]
        return