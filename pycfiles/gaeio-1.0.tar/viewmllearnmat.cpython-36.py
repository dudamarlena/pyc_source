# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\viewmllearnmat.py
# Compiled at: 2019-12-13 23:42:45
# Size of source mod 2**32: 6615 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.gui.plotmllearncurve import plotmllearncurve as gui_plotmllearncurve
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class viewmllearnmat(object):
    learnmat = []
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ViewMlLearnMat):
        ViewMlLearnMat.setObjectName('ViewMlLearnMat')
        ViewMlLearnMat.setFixedSize(710, 460)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/matrix.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ViewMlLearnMat.setWindowIcon(icon)
        self.btncopy = QtWidgets.QPushButton(ViewMlLearnMat)
        self.btncopy.setObjectName('btncopy')
        self.btncopy.setGeometry(QtCore.QRect(520, 10, 80, 30))
        self.btncopy.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/copy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btncopy.setIcon(icon)
        self.btnplot = QtWidgets.QPushButton(ViewMlLearnMat)
        self.btnplot.setObjectName('btnplot')
        self.btnplot.setGeometry(QtCore.QRect(610, 10, 80, 30))
        self.btnplot.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/plot.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnplot.setIcon(icon)
        self.twglearnmat = QtWidgets.QTableWidget(ViewMlLearnMat)
        self.twglearnmat.setObjectName('twglearnmat')
        self.twglearnmat.setGeometry(QtCore.QRect(10, 50, 680, 380))
        self.twglearnmat.setColumnCount(2)
        self.twglearnmat.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.msgbox = QtWidgets.QMessageBox(ViewMlLearnMat)
        self.msgbox.setObjectName('msgbox')
        _center_x = ViewMlLearnMat.geometry().center().x()
        _center_y = ViewMlLearnMat.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ViewMlLearnMat)
        QtCore.QMetaObject.connectSlotsByName(ViewMlLearnMat)

    def retranslateGUI(self, ViewMlLearnMat):
        self.dialog = ViewMlLearnMat
        _translate = QtCore.QCoreApplication.translate
        ViewMlLearnMat.setWindowTitle(_translate('ViewMlLearnMat', 'Learning Matrix'))
        self.btncopy.setText(_translate('ViewMlLearnMat', 'Copy'))
        self.btncopy.clicked.connect(self.clickBtnCopy)
        self.btnplot.setText(_translate('ViewMlLearnMat', 'Plot'))
        self.btnplot.setDefault(True)
        self.btnplot.clicked.connect(self.clickBtnPlot)
        if np.ndim(self.learnmat) == 2 and np.shape(self.learnmat)[1] >= 5:
            self.btncopy.setEnabled(True)
            self.btnplot.setEnabled(True)
            _nrow = np.shape(self.learnmat)[0]
            _ncol = 5
            self.twglearnmat.setRowCount(_nrow)
            self.twglearnmat.setColumnCount(_ncol)
            _colheader = ['Epoch', 'Train. accuracy', 'Valid. accuracy', 'Train. loss', 'Valid loss']
            self.twglearnmat.setHorizontalHeaderLabels(_colheader)
            self.twglearnmat.verticalHeader().hide()
            for i in range(_nrow):
                for j in range(_ncol):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(_translate('ViewMlLearnMat', str(self.learnmat[(i, j)])))
                    if j == 0:
                        item.setText(_translate('ViewMlLearnMat', str(int(self.learnmat[(i, j)]))))
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.twglearnmat.setItem(i, j, item)

    def clickBtnCopy(self):
        self.refreshMsgBox()
        _s = ''
        for i in range(self.twglearnmat.rowCount()):
            for j in range(self.twglearnmat.columnCount()):
                _s = _s + self.twglearnmat.item(i, j).text() + '\t'

            _s = _s + '\n'

        QtGui.QGuiApplication.clipboard().setText(_s)
        if len(_s) > 0:
            QtWidgets.QMessageBox.information(self.msgbox, 'Learning Matrix', 'Learning matrix copied to clipboard')

    def clickBtnPlot(self):
        self.refreshMsgBox()
        _plotmllearncurve = QtWidgets.QDialog()
        _gui = gui_plotmllearncurve()
        _gui.learnmat = self.learnmat
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_plotmllearncurve)
        _plotmllearncurve.exec()
        _plotmllearncurve.show()

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewMlLearnMat = QtWidgets.QWidget()
    gui = viewmllearnmat()
    gui.setupGUI(ViewMlLearnMat)
    ViewMlLearnMat.show()
    sys.exit(app.exec_())