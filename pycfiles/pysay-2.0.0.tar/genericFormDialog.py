# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\Lib\site-packages\pySAXS\guisaxs\qt\genericFormDialog.py
# Compiled at: 2018-08-22 08:43:03
__doc__ = 'from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,\n        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,\n        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,\n        QVBoxLayout)'
from PyQt5 import QtGui, QtCore, QtWidgets
import sys

class genericFormDialog(QtWidgets.QDialog):

    def __init__(self, names=[], values=[], title='', comment=''):
        super(genericFormDialog, self).__init__()
        self.setModal(True)
        self.names = names
        self.values = values
        self.callbacks = None
        self.actives = None
        self.createFormGroupBox(comment)
        self.result = None
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.submitclose)
        buttonBox.rejected.connect(self.reject)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle(title)
        return

    def addItem(self, name='', value='', callback=None, active=True):
        """
        add items with callbacks and active values
        don't worKKKK !!
        """
        self.names.append(name)
        self.values.append(value)
        if self.callbacks is None:
            self.callbacks = [
             callback]
        else:
            self.callbacks.append(callback)
        if self.actives is None:
            self.actives = [
             active]
        else:
            self.actives.append(active)
        print self.names
        return

    def submitclose(self):
        self.result = []
        for i in range(self.layout.rowCount()):
            self.result.append(self.edtType[i](self.edtList[i].text()))

        self.accept()

    def getResult(self):
        return self.result

    def createFormGroupBox(self, comment=''):
        self.formGroupBox = QtWidgets.QGroupBox(comment)
        self.edtList = []
        self.edtType = []
        self.layout = QtWidgets.QFormLayout()
        self.layout.setLabelAlignment(QtCore.Qt.AlignRight)
        for i in range(len(self.names)):
            name = self.names[i]
            if i < len(self.values):
                val = self.values[i]
            else:
                val = ''
            edt = QtWidgets.QLineEdit(str(val))
            if type(val) == type(1):
                validator = QtGui.QIntValidator()
                edt.setValidator(validator)
                edt.textChanged.connect(self.check_state)
                edt.textChanged.emit(edt.text())
            elif type(val) == type(1.0):
                validator = QtGui.QDoubleValidator()
                edt.setValidator(validator)
                edt.textChanged.connect(self.check_state)
                edt.textChanged.emit(edt.text())
            self.edtType.append(type(val))
            self.edtList.append(edt)
            self.layout.addRow(QtWidgets.QLabel(name + ' :'), edt)

        self.formGroupBox.setLayout(self.layout)

    def check_state(self, *args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#c4df9b'
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a'
        else:
            color = '#f6989d'
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = genericFormDialog(title='test', names=['name', 'ship', 'Movie#'], values=['Jack Sparrow', 'Black Pearl', 1.0])
    sys.exit(dialog.exec_())