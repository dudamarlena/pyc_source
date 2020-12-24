# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pydosh/models/accountsModel.py
# Compiled at: 2014-02-11 15:09:41
import re, os, csv, hashlib, codecs
from PySide import QtCore, QtGui, QtSql
from pydosh import enum
from pydosh import currency, utils
from pydosh.database import db
import pydosh.pydosh_rc

class AccountEditModel(QtSql.QSqlTableModel):

    def __init__(self, parent=None):
        super(AccountEditModel, self).__init__(parent=parent)

    def data(self, item, role=QtCore.Qt.DisplayRole):
        if not item.isValid():
            return None
        else:
            if role == QtCore.Qt.ForegroundRole and self.isDirty(item):
                return QtGui.QColor(255, 165, 0)
            return super(AccountEditModel, self).data(item, role)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole and index.data(QtCore.Qt.DisplayRole) == value:
            return False
        return super(AccountEditModel, self).setData(index, value, role)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if section == enum.kAccountTypeColumn_AccountName:
                return 'Account Name'
            if section == enum.kAccountTypeColumn_DateField:
                return 'Date'
            if section == enum.kAccountTypeColumn_DescriptionField:
                return 'Description'
            if section == enum.kAccountTypeColumn_CreditField:
                return 'Credit'
            if section == enum.kAccountTypeColumn_DebitField:
                return 'Debit'
            if section == enum.kAccountTypeColumn_CurrencySign:
                return 'Currency sign'
            if section == enum.kAccountTypeColumn_DateFormat:
                return 'Date formats'
        return