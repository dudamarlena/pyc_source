# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pydosh/delegates/accountDelegate.py
# Compiled at: 2014-02-11 15:09:41
from PySide import QtGui, QtCore
from pydosh import enum

class AccountDelegate(QtGui.QItemDelegate):

    def __init__(self, parent=None):
        super(AccountDelegate, self).__init__(parent=parent)

    def createEditor(self, parent, option, index):
        lineEdit = QtGui.QLineEdit(parent=parent)
        pattern = None
        if index.column() in (
         enum.kAccountTypeColumn_DateField,
         enum.kAccountTypeColumn_DescriptionField,
         enum.kAccountTypeColumn_CreditField,
         enum.kAccountTypeColumn_DebitField):
            pattern = QtCore.QRegExp('[0-9]+')
        elif index.column() == enum.kAccountTypeColumn_DateFormat:
            pattern = QtCore.QRegExp('[dMy/]+')
        elif index.column() == enum.kAccountTypeColumn_CurrencySign:
            pattern = QtCore.QRegExp('-1|1')
        if pattern:
            lineEdit.setValidator(QtGui.QRegExpValidator(pattern))
        return lineEdit

    def setModelData(self, editor, model, index):
        if not index.isValid():
            return
        if editor:
            model.setData(index, editor.text())

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)