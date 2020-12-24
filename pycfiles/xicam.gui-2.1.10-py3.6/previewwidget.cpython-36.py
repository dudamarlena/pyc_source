# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\gui\widgets\previewwidget.py
# Compiled at: 2018-05-17 15:54:06
# Size of source mod 2**32: 2037 bytes
from qtpy.QtCore import QSize
from qtpy.QtGui import QFont
from qtpy.QtWidgets import QSizePolicy
from pyqtgraph import ImageItem, TextItem, GraphicsLayoutWidget
import os
from xicam.core.data import NonDBHeader
import numpy as np

class PreviewWidget(GraphicsLayoutWidget):

    def __init__(self):
        super(PreviewWidget, self).__init__()
        self.setMinimumHeight(250)
        self.setMinimumWidth(250)
        self.view = self.addViewBox(lockAspect=True, enableMenu=False)
        self.imageitem = ImageItem()
        self.textitem = TextItem(anchor=(0.5, 0))
        self.textitem.setFont(QFont('Zero Threes'))
        self.imgdata = None
        self.view.addItem(self.imageitem)
        self.view.addItem(self.textitem)
        self.textitem.hide()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def sizeHint(self):
        return QSize(250, 250)

    def preview_header(self, header: NonDBHeader):
        try:
            data = header.meta_array()[0]
            self.setImage(data)
        except IndexError:
            self.imageitem.clear()
            self.setText('UNKNOWN DATA FORMAT')

    def setImage(self, imgdata):
        self.imageitem.clear()
        self.textitem.hide()
        self.imgdata = imgdata
        self.imageitem.setImage((np.rot90(np.log(self.imgdata * (self.imgdata > 0) + (self.imgdata < 1)), 3)), autoLevels=True)
        self.view.autoRange()

    def setText(self, text):
        self.textitem.setText(text)
        self.imageitem.clear()
        self.textitem.setVisible(True)
        self.view.autoRange()