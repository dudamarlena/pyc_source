# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\base\tpay.py
# Compiled at: 2012-10-05 10:07:38
from __future__ import absolute_import, print_function, unicode_literals
import PySide.QtCore as _qc
from PySide import QtCore
import banta.db as _db, banta.packages as _pack, banta.utils

class TPayModel(_qc.QAbstractTableModel):
    HEADERS = (
     _qc.QT_TRANSLATE_NOOP(b'typepay', b'Nombre'),
     _qc.QT_TRANSLATE_NOOP(b'typepay', b'Recargo'))

    def __init__(self, parent=None):
        _qc.QAbstractTableModel.__init__(self, parent)
        self.tr = banta.utils.unitr(self.trUtf8)

    def rowCount(self, parent=None):
        return len(_db.DB.typePays)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=0):
        if not index.isValid():
            return
        else:
            row = index.row()
            if row >= len(_db.DB.typePays):
                return
            if role not in (_qc.Qt.DisplayRole, _qc.Qt.EditRole):
                return
            col = index.column()
            tp = _db.DB.typePays[row]
            if col == 0:
                return tp.name
            if col == 1:
                return tp.markup
            return

    def headerData(self, section=0, orientation=None, role=0):
        if role != _qc.Qt.DisplayRole:
            return
        else:
            if orientation == _qc.Qt.Horizontal:
                return self.tr(self.HEADERS[section])
            else:
                return str(section)

            return

    def flags(self, index=None):
        if index.isValid():
            return _qc.Qt.ItemIsEditable | _qc.Qt.ItemIsEnabled | _qc.Qt.ItemIsSelectable
        return _qc.Qt.ItemIsEnabled

    def setData(self, index=None, value=None, role=0):
        if index.isValid() and role == _qc.Qt.EditRole:
            tp = _db.DB.typePays[index.row()]
            if index.column() == 0:
                tp.name = value
            elif index.column() == 1:
                tp.markup = float(value)
            _db.DB.commit()
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, index=None):
        self.beginInsertRows(_qc.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            _db.DB.typePays.append(_db.models.TypePay(b''))

        _db.DB.commit()
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, index=None):
        self.beginRemoveRows(_qc.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            del _db.DB.typePays[position]

        _db.DB.commit()
        self.endRemoveRows()
        return True


class TPay(_pack.GenericModule):
    REQUIRES = (
     _pack.GenericModule.P_ADMIN,)
    NAME = b'pay types'

    def __init__(self, app):
        super(TPay, self).__init__(app)
        self.model = TPayModel()
        self.app.window.cb_tpay.setModel(self.model)

    def load(self):
        self.dialog = self.app.uiLoader.load(b':/data/ui/tpay.ui')
        self.dialog.tr = banta.utils.unitr(self.dialog.trUtf8)
        self.app.settings.tabWidget.addTab(self.dialog, self.dialog.tr(b'Tipos de Pago'))
        self.dialog.v_tpay.setModel(self.model)
        self.dialog.bTPNew.clicked.connect(self.new)
        self.dialog.bTPSearch.clicked.connect(self.search)
        self.dialog.bTPDelete.clicked.connect(self.delete)

    @QtCore.Slot()
    def new(self):
        self.model.insertRows(0, 1)

    @QtCore.Slot()
    def search(self):
        text = self.dialog.eTPName.text()
        self.dialog.v_tpay.selectRow(-1)
        for i, tp in enumerate(_db.DB.typePays):
            if text in tp.name.lower():
                self.dialog.v_tpay.selectRow(i)
                break

    @QtCore.Slot()
    def delete(self):
        selected = self.dialog.v_tpay.selectedIndexes()
        if not selected:
            return
        r = selected[0].row()
        self.model.removeRows(r, 1)