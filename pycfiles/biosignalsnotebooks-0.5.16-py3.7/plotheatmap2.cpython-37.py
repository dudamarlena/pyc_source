# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\waves\plotheatmap2.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 567 bytes


def plotheatmap2(s, valmin, valmax, points=100):
    import numpy as np
    import matplotlib.cm as cm
    import matplotlib.mlab as mlab
    import matplotlib.pylab as plt
    x = range(1, len(s))
    y = np.linspace(valmin, valmax, points)
    X, Y = np.meshgrid(x, y)
    Z = mlab.bivariate_normal(X, Y) * 0.0
    for i in range(len(s)):
        Z1 = mlab.bivariate_normal(X, Y, 3.0, 3.0, i, s[i])
        Z = Z1 + Z

    im = plt.imshow(Z, interpolation='bilinear', cmap=(cm.gray), origin='lower')
    return Z