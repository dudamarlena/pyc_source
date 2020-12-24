# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/qt/showimagedialog.py
# Compiled at: 2011-04-23 08:43:29
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_showimagedialog import Ui_ShowImageDialog
logger = logging.getLogger('qtshowimagedialog')

class QtShowImageDialog(Ui_ShowImageDialog, QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.size_hint = QSize(10, 10)

    def show_image(self, pixmap):
        self.labelImage.setPixmap(pixmap)
        self.size_hint = pixmap.size()
        self.labelImage.adjustSize()
        self.scrollAreaWidgetContents.adjustSize()
        self.scrollArea.adjustSize()
        self.adjustSize()

    def sizeHint(self):
        return self.size_hint