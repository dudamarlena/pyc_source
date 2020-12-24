# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/qt/ui_showimagedialog.py
# Compiled at: 2011-04-23 08:43:29
from PyQt4 import QtCore, QtGui

class Ui_ShowImageDialog(object):

    def setupUi(self, ShowImageDialog):
        ShowImageDialog.setObjectName('ShowImageDialog')
        ShowImageDialog.resize(384, 337)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ShowImageDialog.sizePolicy().hasHeightForWidth())
        ShowImageDialog.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(ShowImageDialog)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.scrollArea = QtGui.QScrollArea(ShowImageDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 370, 323))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.labelImage = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelImage.sizePolicy().hasHeightForWidth())
        self.labelImage.setSizePolicy(sizePolicy)
        self.labelImage.setText('')
        self.labelImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelImage.setObjectName('labelImage')
        self.horizontalLayout_2.addWidget(self.labelImage)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.retranslateUi(ShowImageDialog)
        QtCore.QMetaObject.connectSlotsByName(ShowImageDialog)

    def retranslateUi(self, ShowImageDialog):
        ShowImageDialog.setWindowTitle(QtGui.QApplication.translate('ShowImageDialog', 'Image', None, QtGui.QApplication.UnicodeUTF8))
        return