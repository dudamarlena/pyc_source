# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/gif.py
# Compiled at: 2020-05-03 00:26:03
# Size of source mod 2**32: 628 bytes
"""
Module that contains implementation for custom PySide/PyQt windows
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *

class GifLabel(QLabel, object):

    def __init__(self, gif_file):
        super(GifLabel, self).__init__('Name')
        self._movie = QMovie(gif_file, QByteArray(), self)
        self._movie.setCacheMode(QMovie.CacheAll)
        self._movie.setSpeed(100)
        self.setMovie(self._movie)
        self.setAlignment(Qt.AlignCenter)
        self._movie.start()