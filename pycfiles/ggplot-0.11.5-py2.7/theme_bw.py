# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/themes/theme_bw.py
# Compiled at: 2016-07-11 10:52:39
from .theme_gray import theme_gray

class theme_bw(theme_gray):
    """
    White background w/ black gridlines
    """

    def __init__(self):
        super(theme_bw, self).__init__()
        self._rcParams['axes.facecolor'] = 'white'