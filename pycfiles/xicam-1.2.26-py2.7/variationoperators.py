# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\variationoperators.py
# Compiled at: 2019-03-07 15:21:12
import collections, numpy as np, loader
from scipy import signal
import integration, writer

def chisquared(data, t, roi):
    current = data[t].astype(float)
    previous = data[(t - 1)].astype(float)
    return np.sum(roi * np.square(current - previous))


def imgmax(data, t, roi):
    current = data[t].astype(float)
    return (roi * current).max()


def qmax(data, t, roi):
    current = data[t]
    q, I = integration.radialintegratepyFAI(current, cut=roi)[:2]
    return q[np.argmax(I)]


def fit_mean(data, t, roi):
    current = data[t]
    q, I = integration.radialintegratepyFAI(current, cut=roi)[:2]
    from astropy.modeling import models, fitting
    qmin = q[(np.array(I) != 0).argmax()]
    qmax = q[(len(I) - 1 - (np.array(I) != 0)[::-1].argmax())]
    g_init = models.Gaussian1D(amplitude=np.array(I).max(), mean=(qmax + qmin) / 2, stddev=(qmax - qmin) / 4)
    fit_g = fitting.LevMarLSQFitter()
    g = fit_g(g_init, q, I)
    return g.mean.value


def fit_stddev(data, t, roi):
    current = data[t]
    q, I = integration.radialintegratepyFAI(current, cut=roi)[:2]
    from astropy.modeling import models, fitting
    qmin = q[(np.array(I) != 0).argmax()]
    qmax = q[(len(I) - 1 - (np.array(I) != 0)[::-1].argmax())]
    g_init = models.Gaussian1D(amplitude=np.array(I).max(), mean=(qmax + qmin) / 2, stddev=(qmax - qmin) / 4)
    fit_g = fitting.LevMarLSQFitter()
    g = fit_g(g_init, q, I)
    return g.stddev.value


def gaussian_fit(data, t, roi):
    current = data[t]
    q, I = integration.radialintegratepyFAI(current, cut=roi)[:2]
    from astropy.modeling import models, fitting
    qmin = q[(np.array(I) != 0).argmax()]
    qmax = q[(len(I) - 1 - (np.array(I) != 0)[::-1].argmax())]
    g_init = models.Gaussian1D(amplitude=np.array(I).max(), mean=(qmax + qmin) / 2, stddev=(qmax - qmin) / 4)
    fit_g = fitting.LevMarLSQFitter()
    g = fit_g(g_init, q, I)
    return collections.OrderedDict([
     (
      'stddev', g.stddev.value), ('mean', g.mean.value), ('Amplitude', g.amplitude.value),
     (
      'chi^2', np.average((g(q) - I) ** 2))])


def absdiff(data, t, roi):
    current = data[t].astype(float)
    previous = data[(t - 1)].astype(float)
    return np.sum(roi * np.abs(current - previous))


def normabsdiff(data, t, roi):
    current = data[t].astype(float)
    previous = data[(t - 1)].astype(float)
    return np.sum(roi * np.abs(current - previous) / previous)


def sumintensity(data, t, roi):
    current = data[t].astype(float)
    return np.sum(roi * current)


def normabsdiffderiv(data, t, roi):
    current = data[t].astype(float)
    previous = data[(t - 1)].astype(float)
    next = data[(t + 1)].astype(float)
    return -np.sum(roi * (np.abs(next - current) / current) + np.sum(np.abs(current - previous) / current))


def chisquaredwithfirst(data, t, roi):
    current = data[t].astype(float)
    first = data[0].astype(float)
    return np.sum(roi * np.square(current.astype(float) - first))


def radialintegration(data, t, roi):
    current = data[t]
    return integration.radialintegratepyFAI(current, cut=roi)[:2]


def angularcorrelationwithfirst(data, t, roi):
    experiment.center = (
     experiment.center[0] / 5, experiment.center[1] / 5)
    currentcake, _, _ = integration.cake(data[t], experiment)
    firstcake, _, _ = integration.cake(data[0], experiment)
    currentchi = np.sum(currentcake * roi, axis=0)
    firstchi = np.sum(firstcake * roi, axis=0)
    return signal.convolve(currentchi, firstchi)


operations = collections.OrderedDict([('Chi Squared', chisquared),
 (
  'Max', imgmax),
 (
  'Absolute Diff.', absdiff),
 (
  'Norm. Abs. Diff.', normabsdiff),
 (
  'Sum Intensity', sumintensity),
 (
  'Norm. Abs. Derivative', normabsdiffderiv),
 (
  'Chi Squared w/First Frame', chisquaredwithfirst),
 (
  'Angular autocorrelation w/First Frame', angularcorrelationwithfirst),
 (
  'Radial Integration', radialintegration),
 (
  'Q at peak max', qmax),
 (
  'Q at peak fit max', fit_mean),
 (
  'Peak Fit Std. Dev.', fit_stddev),
 (
  'Gaussian Q Fit', gaussian_fit)])
experiment = None