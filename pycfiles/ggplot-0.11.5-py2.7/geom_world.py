# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_world.py
# Compiled at: 2016-08-09 11:05:39
from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.image as mpimg, os, sys
from .geom import geom
_ROOT = os.path.abspath(os.path.dirname(__file__))

class geom_world(geom):
    """
    Planet Earth

    Parameters
    ----------
    alpha:
        transparency of bird

    Examples
    --------
    """
    DEFAULT_AES = {b'alpha': 0.5}
    DEFAULT_PARAMS = {}

    def plot(self, ax, data, _aes):
        data, _aes = self._update_data(data, _aes)
        params = self._get_plot_args(data, _aes)
        img = mpimg.imread(os.path.join(_ROOT, b'world.png'))
        ax.imshow(img, **params)