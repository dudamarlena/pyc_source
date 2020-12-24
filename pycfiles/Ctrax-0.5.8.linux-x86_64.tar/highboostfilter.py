# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/highboostfilter.py
# Compiled at: 2013-09-24 00:46:30
import numpy, numpy.fft

def highboostfilter(sze, cutoff, n, boost):
    if cutoff < 0.0 or cutoff > 0.5:
        raise ValueError, 'cutoff frequency must be between 0 and 0.5'
    if numpy.remainder(n, 1) != 0 or n < 1:
        raise ValueError, 'n must be an integer >= 1'
    if boost >= 1:
        return (1 - 1.0 / boost) * highpassfilter(sze, cutoff, n) + 1.0 / boost
    else:
        return (1 - boost) * lowpassfilter(sze, cutoff, n) + boost


def highpassfilter(sze, cutoff, n):
    if cutoff < 0.0 or cutoff > 0.5:
        raise ValueError, 'cutoff frequency must be between 0 and 0.5'
    if numpy.remainder(n, 1) != 0 | n < 1:
        raise ValueError, 'n must be an integer >= 1'
    return 1 - lowpassfilter(sze, cutoff, n)


def lowpassfilter(sze, cutoff, n):
    if cutoff < 0 or cutoff > 0.5:
        raise ValueError, 'cutoff frequency must be between 0 and 0.5'
    if numpy.remainder(n, 1) != 0 or cutoff > 0.5:
        raise ValueError, 'n must be an integer >= 1'
    if len(sze) == 1:
        rows = cols = sze
    else:
        rows = sze[0]
        cols = sze[1]
    if numpy.mod(cols, 2) != 0:
        xrng = numpy.arange(-(cols - 1) / 2.0, (cols - 1) / 2.0 + 1) / (cols - 1)
    else:
        xrng = numpy.arange(-cols / 2.0, cols / 2.0) / cols
    if numpy.mod(rows, 2) != 0:
        yrng = numpy.arange(-(rows - 1) / 2.0, (rows - 1) / 2.0 + 1) / (rows - 1)
    else:
        yrng = numpy.arange(-rows / 2.0, rows / 2.0) / rows
    x = numpy.zeros((len(yrng), len(xrng)))
    for rr in range(len(yrng)):
        x[rr, :] = xrng[:]

    y = numpy.zeros((len(yrng), len(xrng)))
    for cc in range(len(xrng)):
        y[:, cc] = yrng[:]

    radius = numpy.sqrt(x ** 2 + y ** 2)
    return numpy.fft.ifftshift(1.0 / (1 + (radius / cutoff) ** (2 * n)))