# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\editseispointset.py
# Compiled at: 2020-03-28 16:26:08
# Size of source mod 2**32: 10349 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.pointset.analysis import analysis as point_ays
from cognitivegeo.src.vis.messager import messager as vis_msg
from cognitivegeo.src.gui.rtrvseisprop import rtrvseisprop as gui_rtrvseisprop
from cognitivegeo.src.gui.calculator import calculator as gui_calculator
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class editseispointset(object):
    seispointsetdata = {}
    rootpath = ''
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, EditSeisPointSet):
        EditSeisPointSet.setObjectName('EditSeisPointSet')
        EditSeisPointSet.setFixedSize(300, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EditSeisPointSet.setWindowIcon(icon)
        self.lblattrib = QtWidgets.QLabel(EditSeisPointSet)
        self.lblattrib.setObjectName('lblattrib')
        self.lblattrib.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(EditSeisPointSet)
        self.lwgattrib.setObjectName('lwgattrib')
        self.lwgattrib.setGeometry(QtCore.QRect(10, 50, 280, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblaction = QtWidgets.QLabel(EditSeisPointSet)
        self.lblaction.setObjectName('lblaction')
        self.lblaction.setGeometry(QtCore.QRect(110, 270, 40, 30))
        self.cbbaction = QtWidgets.QComboBox(EditSeisPointSet)
        self.cbbaction.setObjectName('cbbaction')
        self.cbbaction.setGeometry(QtCore.QRect(160, 270, 130, 30))
        self.ldtrename = QtWidgets.QLineEdit(EditSeisPointSet)
        self.ldtrename.setObjectName('ldtrename')
        self.ldtrename.setGeometry(QtCore.QRect(160, 310, 130, 30))
        self.btnedit = QtWidgets.QPushButton(EditSeisPointSet)
        self.btnedit.setObjectName('btnedit')
        self.btnedit.setGeometry(QtCore.QRect(100, 370, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/ok.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(EditSeisPointSet)
        self.msgbox.setObjectName('msgbox')
        _center_x = EditSeisPointSet.geometry().center().x()
        _center_y = EditSeisPointSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(EditSeisPointSet)
        QtCore.QMetaObject.connectSlotsByName(EditSeisPointSet)

    def retranslateGUI(self, EditSeisPointSet):
        self.dialog = EditSeisPointSet
        _translate = QtCore.QCoreApplication.translate
        EditSeisPointSet.setWindowTitle(_translate('EditSeisPointSet', 'Edit Seismic/PointSet'))
        self.lblattrib.setText(_translate('EditSeisPointSet', 'List of available properties:'))
        self.lblaction.setText(_translate('EditSeisPointSet', 'Action:'))
        self.cbbaction.addItems(['Copy', 'Rename', 'Delete', 'Add', 'Math'])
        self.cbbaction.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/copy.png')))
        self.cbbaction.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/rename.png')))
        self.cbbaction.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/delete.png')))
        self.cbbaction.setItemIcon(3, QtGui.QIcon(os.path.join(self.iconpath, 'icons/retrieve.png')))
        self.cbbaction.setItemIcon(4, QtGui.QIcon(os.path.join(self.iconpath, 'icons/math.png')))
        self.cbbaction.setCurrentIndex(4)
        self.cbbaction.currentIndexChanged.connect(self.changeCbbAction)
        self.ldtrename.setText(_translate('EditSeisPointSet', ''))
        self.ldtrename.setVisible(False)
        self.btnedit.setText(_translate('EditSeisPointSet', 'Apply'))
        self.btnedit.clicked.connect(self.clickBtnEditSeisPointSet)
        self.refreshLwgAttrib()

    def changeCbbAction(self):
        if self.cbbaction.currentIndex() == 1:
            self.ldtrename.setVisible(True)
        else:
            self.ldtrename.setText('')
            self.ldtrename.setVisible(False)
        if self.cbbaction.currentIndex() == 2:
            self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        else:
            self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def clickBtnEditSeisPointSet(self):
        self.refreshMsgBox()
        _attriblist = self.lwgattrib.selectedItems()
        if self.cbbaction.currentIndex() != 3:
            if len(_attriblist) < 1:
                vis_msg.print('ERROR in EditSeisPointSet: No property selected for editing', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Edit Seismic/PointSet', 'No property selected for editing')
                return
        if self.cbbaction.currentIndex() == 0:
            self.seispointsetdata[_attriblist[0].text() + '_copy'] = self.seispointsetdata[_attriblist[0].text()].copy()
        if self.cbbaction.currentIndex() == 1:
            if len(self.ldtrename.text()) < 1:
                vis_msg.print('ERROR in EditSeisPointSet: No name specified for rename', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Edit Seismic/PointSet', 'No name specified for rename')
                return
            if self.ldtrename.text() in self.seispointsetdata.keys():
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Edit Seismic/PointSet', self.ldtrename.text() + ' already exists. Overwrite?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.seispointsetdata[self.ldtrename.text()] = self.seispointsetdata[_attriblist[0].text()]
            self.seispointsetdata.pop(_attriblist[0].text())
        if self.cbbaction.currentIndex() == 2:
            for _i in range(len(_attriblist)):
                self.seispointsetdata.pop(_attriblist[_i].text())

        if self.cbbaction.currentIndex() == 3:
            _rtrvprop = QtWidgets.QDialog()
            _gui = gui_rtrvseisprop()
            _gui.pointsetdata = self.seispointsetdata.copy()
            _gui.rootpath = self.rootpath
            _gui.setupGUI(_rtrvprop)
            _rtrvprop.exec()
            self.seispointsetdata = _gui.pointsetdata.copy()
            _rtrvprop.show()
        if self.cbbaction.currentIndex() == 4:
            _math = QtWidgets.QDialog()
            _gui = gui_calculator()
            _gui.data = self.seispointsetdata[_attriblist[0].text()].copy()
            _gui.setupGUI(_math)
            _math.exec()
            self.seispointsetdata[_attriblist[0].text()] = _gui.data.copy()
            _math.show()
        self.refreshLwgAttrib()

    def refreshLwgAttrib(self):
        self.lwgattrib.clear()
        if self.checkSeisPointSet() is True:
            for i in sorted(self.seispointsetdata.keys()):
                if i != 'Inline' and i != 'Crossline' and i != 'Z':
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(i)
                    self.lwgattrib.addItem(item)

            if 'Inline' in self.seispointsetdata.keys():
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText('Inline')
                self.lwgattrib.addItem(item)
            if 'Crossline' in self.seispointsetdata.keys():
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText('Crossline')
                self.lwgattrib.addItem(item)
            if 'Z' in self.seispointsetdata.keys():
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText('Z')
                self.lwgattrib.addItem(item)

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))

    def checkSeisPointSet(self):
        return point_ays.checkPointSet(self.seispointsetdata)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditSeisPointSet = QtWidgets.QWidget()
    gui = editseispointset()
    gui.setupGUI(EditSeisPointSet)
    EditSeisPointSet.show()
    sys.exit(app.exec_())