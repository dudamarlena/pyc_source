# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\gaeio\src\gui\exportpointsetfile.py
# Compiled at: 2020-04-25 14:58:02
# Size of source mod 2**32: 7619 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.pointset.inputoutput import inputoutput as pointset_io
from gaeio.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class exportpointsetfile(object):
    pointsetdata = {}
    rootpath = ''
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ExportPointSetFile):
        ExportPointSetFile.setObjectName('ExportPointSetFile')
        ExportPointSetFile.setFixedSize(400, 340)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/copy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ExportPointSetFile.setWindowIcon(icon)
        self.lblpoint = QtWidgets.QLabel(ExportPointSetFile)
        self.lblpoint.setObjectName('lblpoint')
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgpoint = QtWidgets.QListWidget(ExportPointSetFile)
        self.lwgpoint.setObjectName('lwgpoint')
        self.lwgpoint.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwgpoint.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblsave = QtWidgets.QLabel(ExportPointSetFile)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 230, 50, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportPointSetFile)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(70, 230, 250, 30))
        self.btnsave = QtWidgets.QPushButton(ExportPointSetFile)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 230, 60, 30))
        self.btnexportnpy = QtWidgets.QPushButton(ExportPointSetFile)
        self.btnexportnpy.setObjectName('btnexportnpy')
        self.btnexportnpy.setGeometry(QtCore.QRect(120, 280, 160, 30))
        self.btnexportnpy.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ExportPointSetFile)
        self.msgbox.setObjectName('msgbox')
        _center_x = ExportPointSetFile.geometry().center().x()
        _center_y = ExportPointSetFile.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ExportPointSetFile)
        QtCore.QMetaObject.connectSlotsByName(ExportPointSetFile)

    def retranslateGUI(self, ExportPointSetFile):
        self.dialog = ExportPointSetFile
        _translate = QtCore.QCoreApplication.translate
        ExportPointSetFile.setWindowTitle(_translate('ExportPointSetFile', 'Export PointSet File'))
        self.lblpoint.setText(_translate('ExportPointSetFile', 'Select output pointsets:'))
        if len(self.pointsetdata.keys()) > 0:
            for i in sorted(self.pointsetdata.keys()):
                item = QtWidgets.QListWidgetItem(self.lwgpoint)
                item.setText(_translate('ExportPointSetFile', i))
                self.lwgpoint.addItem(item)

            self.lwgpoint.selectAll()
        self.lblsave.setText(_translate('ExportPointSetFile', 'Save as:'))
        self.ldtsave.setText(_translate('ExportPointSetFile', ''))
        self.btnsave.setText(_translate('ExportPointSetFile', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexportnpy.setText(_translate('ExportPointSetFile', 'Export PointSet File'))
        self.btnexportnpy.clicked.connect(self.clickBtnExportPointSetFile)

    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select PointSet File', (self.rootpath), filter='PointSet Ascii files (*.txt);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])

    def clickBtnExportPointSetFile(self):
        self.refreshMsgBox()
        _pointlist = self.lwgpoint.selectedItems()
        if len(_pointlist) < 1:
            vis_msg.print('ERROR in ExportPointSetFile; No pointset selected for export', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Export PointSet FIle', 'No pointset selected for export')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ERROR in ExportPointSetFile: No name specified for export', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Export PointSet File', 'No name specified for export')
            return
        print('ExportPointSetFile: Export %d pointsets' % len(_pointlist))
        _savepath = os.path.split(self.ldtsave.text())[0]
        _savename = os.path.split(self.ldtsave.text())[1]
        if len(_pointlist) > 1:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export PointSet File', 'Warning: For exporting >=2 pointset, property name used as file name. Continue?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return
        for i in range(len(_pointlist)):
            if len(_pointlist) > 1:
                _savename = _pointlist[i].text()
            pointset_io.writePointSetToAscii(pointset=(self.pointsetdata[_pointlist[i].text()]), asciifile=(os.path.join(_savepath, _savename)),
              property_list=(list(self.pointsetdata[_pointlist[i].text()].keys())))

        QtWidgets.QMessageBox.information(self.msgbox, 'Export PointSet File', str(len(_pointlist)) + ' pointsets exported as Ascii File successfully')

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportPointSetFile = QtWidgets.QWidget()
    gui = exportpointsetfile()
    gui.setupGUI(ExportPointSetFile)
    ExportPointSetFile.show()
    sys.exit(app.exec_())