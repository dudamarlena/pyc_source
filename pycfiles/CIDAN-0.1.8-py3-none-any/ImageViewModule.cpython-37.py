# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/ImageView/ImageViewModule.py
# Compiled at: 2020-04-22 00:59:57
# Size of source mod 2**32: 1923 bytes
from pyqtgraph import ImageView
from PySide2.QtWidgets import *
from PySide2.QtCore import *

class ImageViewModule(QFrame):

    def __init__(self, main_widget, histogram=True, roi=True):
        super().__init__()
        self.main_window = main_widget
        self.setStyleSheet('ImageViewModule {margin:0px; border:0px  solid rgb(50, 65, 75); padding: 0px;} ')
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.image_view = ImageView()
        self.image_view.ui.menuBtn.hide()
        if not histogram:
            self.image_view.ui.histogram.hide()
        if not roi:
            self.image_view.ui.roiBtn.hide()
        self.layout.addWidget(self.image_view)

    def setImage(self, data):
        self.image_view.setImage(data, levelMode='mono', autoRange=True, autoLevels=True,
          autoHistogramRange=True)