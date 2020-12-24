# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/utils/colormaputil.py
# Compiled at: 2018-11-09 15:08:51
"""
Credit & source: https://gist.github.com/salotz/4f585aac1adb6b14305c
"""
from __future__ import print_function, division, absolute_import
import numpy as np
from matplotlib import pyplot as pl, cm, colors
__version__ = '2013-12-19 dec denis'

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    """ mycolormap = truncate_colormap(
            cmap name or file or ndarray,
            minval=0.2, maxval=0.8 ): subset
            minval=1, maxval=0 )    : reverse
    by unutbu http://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
    """
    cmap = get_cmap(cmap)
    name = '%s-trunc-%.2g-%.2g' % (cmap.name, minval, maxval)
    return colors.LinearSegmentedColormap.from_list(name, cmap(np.linspace(minval, maxval, n)))


def stack_colormap(A, B, n=256):
    """ low half -> A colors, high half -> B colors """
    A = get_cmap(A)
    B = get_cmap(B)
    name = '%s-%s' % (A.name, B.name)
    lin = np.linspace(0, 1, n)
    return array_cmap(np.vstack((A(lin), B(lin))), name, n=n)


def get_cmap(cmap, name=None, n=256):
    """ in: a name "Blues" "BuGn_r" ... of a builtin cmap (case-sensitive)
        or a filename, np.loadtxt() n x 3 or 4  ints 0..255 or floats 0..1
        or a cmap already
        or a numpy array.
        See http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps
        or in IPython, pl.cm.<tab>
    """
    if isinstance(cmap, colors.Colormap):
        return cmap
    else:
        if isinstance(cmap, str):
            if cmap in cm.cmap_d:
                return pl.get_cmap(cmap)
            A = np.loadtxt(cmap, delimiter=None)
            name = name or cmap.split('/')[(-1)].split('.')[0]
        else:
            A = cmap
        return array_cmap(A, name, n=n)


def array_cmap(A, name=None, n=256):
    """ numpy array -> a cmap, matplotlib.colors.Colormap
        n x 3 or 4  ints 0 .. 255 or floats 0 ..1
    """
    A = np.asanyarray(A)
    assert A.ndim == 2 and A.shape[1] in (3, 4), 'array must be n x 3 or 4, not %s' % str(A.shape)
    Amin, Amax = A.min(), A.max()
    if not (A.dtype.kind == 'i' and 0 <= Amin < Amax <= 255):
        raise AssertionError('Amin %d  Amax %d must be in 0 .. 255' % (Amin, Amax))
        A = A / 255.0
    else:
        assert 0 <= Amin < Amax <= 1, 'Amin %g  Amax %g must be in 0 .. 1' % (Amin, Amax)
    return colors.LinearSegmentedColormap.from_list(name or 'noname', A, N=n)


def save_cmap(outfile, cmap):
    """ -> a file of 256 x 4 ints 0 .. 255
        to load it, np.loadtxt() or get_cmap( filename )
    """
    cmap = get_cmap(cmap)
    A = cmap(np.linspace(0, 1, 256))
    np.savetxt(outfile, A * 255, fmt='%4.0f', header='colormap %s' % cmap.name)


def band_colormap(cmap, nband=10):
    """ -> a colormap with e.g. 10 bands """
    cmap = get_cmap(cmap)
    h = 0.5 / nband
    A = cmap(np.linspace(h, 1 - h, nband))
    name = '%s-band-%d' % (cmap.name, nband)
    return array_cmap(A, name, n=nband)


cmap_brown = truncate_colormap(pl.cm.PuOr, minval=0.5, maxval=0)
cmap_bluebrown = stack_colormap('Blues_r', cmap_brown)
cmap_bluebrown10 = band_colormap(cmap_bluebrown, 10)
if __name__ == '__main__':
    import sys
    cmap = cmap_bluebrown10
    bw = array_cmap([[0.0, 0, 0], [1, 1, 1]], name='bw', n=2)
    plot = 0
    exec ('\n').join(sys.argv[1:])
    np.set_printoptions(2, threshold=100, edgeitems=10, linewidth=100, suppress=True)
    print(cmap.name, '\n', cmap(np.arange(120, 136) / 256).T)
    save_cmap(cmap.name + '.tmp', cmap)
    if plot:
        A = np.arange(64).reshape((8, 8))
        im = pl.imshow(A, cmap=cmap, interpolation='nearest')
        pl.colorbar(im)
pl.show()