# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\gui\viewsegytextualheader.py
# Compiled at: 2019-12-13 23:42:45
# Size of source mod 2**32: 3969 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.seismic.inputoutput import inputoutput as seis_io
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class viewsegytextualheader(object):
    segyfile = ''
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ViewSegyTextualHeader):
        ViewSegyTextualHeader.setObjectName('ViewSegyTextualHeader')
        ViewSegyTextualHeader.setFixedSize(560, 460)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/segy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ViewSegyTextualHeader.setWindowIcon(icon)
        self.lblhelp = QtWidgets.QLabel(ViewSegyTextualHeader)
        self.lblhelp.setObjectName('lblhelp')
        self.lblhelp.setGeometry(QtCore.QRect(460, 10, 80, 30))
        self.lwgheader = QtWidgets.QListWidget(ViewSegyTextualHeader)
        self.lwgheader.setObjectName('lwgheader')
        self.lwgheader.setGeometry(QtCore.QRect(10, 50, 530, 380))
        self.lwgheader.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.msgbox = QtWidgets.QMessageBox(ViewSegyTextualHeader)
        self.msgbox.setObjectName('msgbox')
        _center_x = ViewSegyTextualHeader.geometry().center().x()
        _center_y = ViewSegyTextualHeader.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ViewSegyTextualHeader)
        QtCore.QMetaObject.connectSlotsByName(ViewSegyTextualHeader)

    def retranslateGUI(self, ViewSegyTextualHeader):
        self.dialog = ViewSegyTextualHeader
        _translate = QtCore.QCoreApplication.translate
        ViewSegyTextualHeader.setWindowTitle(_translate('ViewSegyTextualHeader', 'SEG-Y Textual Header'))
        self.lblhelp.setText(_translate('ViewSegyTextualHeader', '<a href="https://seg.org/Portals/0/SEG/News%20and%20Resources/Technical%20Standards/seg_y_rev1.pdf">SEG-Y Format</a>'))
        self.lblhelp.setOpenExternalLinks(True)
        if os.path.exists(self.segyfile):
            _header = seis_io.readSegyTextualHeader(self.segyfile)
            for _i in _header:
                item = QtWidgets.QListWidgetItem(self.lwgheader)
                item.setText(_translate('ViewSegyTextualHeader', _i))
                self.lwgheader.addItem(item)

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewSegyTextualHeader = QtWidgets.QWidget()
    gui = viewsegytextualheader()
    gui.setupGUI(ViewSegyTextualHeader)
    ViewSegyTextualHeader.show()
    sys.exit(app.exec_())