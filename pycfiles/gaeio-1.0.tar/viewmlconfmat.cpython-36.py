# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\geopy\src\gui\viewmlconfmat.py
# Compiled at: 2019-12-06 17:51:50
# Size of source mod 2**32: 5229 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class viewmlconfmat(object):
    confmat = []
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ViewMlConfMat):
        ViewMlConfMat.setObjectName('ViewMlConfMat')
        ViewMlConfMat.setFixedSize(410, 450)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/confmat.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ViewMlConfMat.setWindowIcon(icon)
        self.btncopy = QtWidgets.QPushButton(ViewMlConfMat)
        self.btncopy.setObjectName('btncopy')
        self.btncopy.setGeometry(QtCore.QRect(310, 10, 80, 30))
        self.btncopy.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/copy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btncopy.setIcon(icon)
        self.twgconfmat = QtWidgets.QTableWidget(ViewMlConfMat)
        self.twgconfmat.setObjectName('twgseis')
        self.twgconfmat.setGeometry(QtCore.QRect(10, 50, 380, 380))
        self.twgconfmat.setColumnCount(2)
        self.twgconfmat.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.msgbox = QtWidgets.QMessageBox(ViewMlConfMat)
        self.msgbox.setObjectName('msgbox')
        _center_x = ViewMlConfMat.geometry().center().x()
        _center_y = ViewMlConfMat.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ViewMlConfMat)
        QtCore.QMetaObject.connectSlotsByName(ViewMlConfMat)

    def retranslateGUI(self, ViewMlConfMat):
        self.dialog = ViewMlConfMat
        _translate = QtCore.QCoreApplication.translate
        ViewMlConfMat.setWindowTitle(_translate('ViewMlConfMat', 'Confusion Matrix'))
        self.btncopy.setText(_translate('ViewMlConfMat', 'Copy'))
        self.btncopy.clicked.connect(self.clickBtnCopy)
        if np.ndim(self.confmat) == 2 and np.shape(self.confmat)[0] > 1 and np.shape(self.confmat)[1] > 1:
            self.btncopy.setEnabled(True)
            self.confmat = self.confmat.astype(int)
            _nrow = np.shape(self.confmat)[0]
            _ncol = np.shape(self.confmat)[1]
            self.twgconfmat.setRowCount(_nrow - 1)
            self.twgconfmat.setColumnCount(_ncol - 1)
            _colheader = ['Predicted: ' + str(i) for i in self.confmat[0, 1:]]
            _rowheader = ['True: ' + str(i) for i in self.confmat[1:, 0]]
            self.twgconfmat.setHorizontalHeaderLabels(_colheader)
            self.twgconfmat.setVerticalHeaderLabels(_rowheader)
            for i in range(_nrow - 1):
                for j in range(_ncol - 1):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(_translate('ViewMlConfMat', str(self.confmat[(i + 1, j + 1)])))
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.twgconfmat.setItem(i, j, item)

    def clickBtnCopy(self):
        self.refreshMsgBox()
        _s = ''
        for i in range(self.twgconfmat.rowCount()):
            for j in range(self.twgconfmat.columnCount()):
                _s = _s + self.twgconfmat.item(i, j).text() + '\t'

            _s = _s + '\n'

        QtGui.QGuiApplication.clipboard().setText(_s)
        if len(_s) > 0:
            QtWidgets.QMessageBox.information(self.msgbox, 'Confusion Matrix', 'Confusion matrix copied to clipboard')

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewMlConfMat = QtWidgets.QWidget()
    gui = viewmlconfmat()
    gui.setupGUI(ViewMlConfMat)
    ViewMlConfMat.show()
    sys.exit(app.exec_())