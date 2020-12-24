# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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