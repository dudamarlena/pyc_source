# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/widgets/label.py
# Compiled at: 2020-04-17 19:05:38
# Size of source mod 2**32: 821 bytes
"""
Module that contains widget to create wait spinners
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from Qt.QtCore import *
from Qt.QtWidgets import *

class ThumbnailLabel(QLabel, object):

    def __init__(self, parent=None):
        super(ThumbnailLabel, self).__init__(parent=parent)

    def setPixmap(self, pixmap):
        if pixmap.height() > 55 or pixmap.width() > 80:
            pixmap = pixmap.scaled(QSize(80, 55), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        super(ThumbnailLabel, self).setPixmap(pixmap)