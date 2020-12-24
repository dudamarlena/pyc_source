# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/themes/theme_xkcd.py
# Compiled at: 2016-07-11 10:52:39
from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib as mpl, matplotlib.pyplot as plt
from .theme import theme_base

class theme_xkcd(theme_base):
    """
    xkcd theme

    The theme internaly uses the settings from pyplot.xkcd().

    """

    def __init__(self, scale=1, length=100, randomness=2):
        super(theme_xkcd, self).__init__()
        with plt.xkcd(scale=scale, length=length, randomness=randomness):
            _xkcd = mpl.rcParams.copy()
        for key in mpl._deprecated_map:
            if key in _xkcd:
                del _xkcd[key]

        if b'tk.pythoninspect' in _xkcd:
            del _xkcd[b'tk.pythoninspect']
        self._rcParams.update(_xkcd)

    def __deepcopy__(self, memo):

        class _empty(object):
            pass

        result = _empty()
        result.__class__ = self.__class__
        result.__dict__[b'_rcParams'] = {}
        for k, v in self._rcParams.items():
            try:
                result.__dict__[b'_rcParams'][k] = deepcopy(v, memo)
            except NotImplementedError:
                result.__dict__[b'_rcParams'][k] = copy(v)

        return result