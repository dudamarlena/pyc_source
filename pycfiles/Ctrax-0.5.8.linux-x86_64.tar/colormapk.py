# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/colormapk.py
# Compiled at: 2013-09-24 00:46:30
import numpy as num

def jet(m=64):
    if m == 1:
        J = num.array([0, 0, 0])
        return J
    m = m - 1
    n = int(num.ceil(m / 4.0))
    u = num.concatenate((num.linspace(1.0 / n, 1.0, n),
     num.ones(n - 1),
     num.linspace(1.0, 1.0 / n, n)), 0)
    g = num.ceil(n / 2.0) - int(m % 4 == 1) + num.r_[0:u.size]
    g = g.astype(int)
    r = g + n
    b = g - n
    g = g[(g < m)]
    r = r[(r < m)]
    b = b[(b >= 0)]
    J = num.zeros((m, 3))
    J[(r, 0)] = u[:r.size]
    J[(g, 1)] = u[:g.size]
    J[(b, 2)] = u[-b.size:]
    J = num.concatenate((num.zeros((1, 3)), J), axis=0)
    return J


def colormap_image(imin, cmap=None, cbounds=None):
    assert imin.ndim <= 2
    if cmap is None:
        cmap = jet(64)
    im = imin.astype(num.double)
    if cbounds is not None:
        assert len(cbounds) == 2
        assert cbounds[0] <= cbounds[1]
        im = im.clip(cbounds[0], cbounds[1])
    neginfidx = num.isneginf(im)
    isneginf = num.any(neginfidx)
    posinfidx = num.isposinf(im)
    isposinf = num.any(posinfidx)
    nanidx = num.isnan(im)
    isnan = num.any(nanidx)
    goodidx = [
     num.logical_not(num.logical_or(num.logical_or(neginfidx, posinfidx), nanidx))]
    minv = im[goodidx].min()
    maxv = im[goodidx].max()
    if minv == maxv and minv >= 1.0:
        minv -= 1.0
    elif minv == maxv:
        maxv += 1.0
    dv = maxv - minv
    if isposinf:
        maxv = maxv + dv * 0.025
        im[posinfidx] = maxv
    if isneginf or isnan:
        minv = minv - dv * 0.025
        im[neginfidx] = minv
        im[nanidx] = minv
    im = (im - minv) / (maxv - minv)
    im *= float(cmap.shape[0] - 1)
    im = im.round()
    im = im.astype(int)
    r = cmap[(im, 0)]
    g = cmap[(im, 1)]
    b = cmap[(im, 2)]
    newshape = r.shape + (1, )
    rgb = num.concatenate((num.reshape(r, newshape),
     num.reshape(g, newshape),
     num.reshape(b, newshape)), 2)
    rgb *= 255
    rgb = rgb.astype(num.uint8)
    clim = [
     minv, maxv]
    return (
     rgb, clim)