# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/colormapk.py
# Compiled at: 2008-01-29 20:48:29
import matplotlib, numpy, matplotlib.colors

def colormap_image(imin, cmap=None, cbounds=None):
    assert imin.ndim <= 2
    if cmap is None:
        cmap = matplotlib.cm.jet
    assert isinstance(cmap, matplotlib.colors.Colormap)
    im = imin.astype(numpy.double)
    if cbounds is not None:
        assert len(cbounds) == 2
        assert cbounds[0] <= cbounds[1]
        im = im.clip(cbounds[0], cbounds[1])
    im -= im.min()
    im /= im.max()
    im *= cmap.N - 1.0
    im = im.round()
    im = im.astype(int)
    rgb = cmap(im)
    rgb = rgb[:, :, :-1]
    rgb *= 255
    rgb = rgb.astype(numpy.uint8)
    return rgb