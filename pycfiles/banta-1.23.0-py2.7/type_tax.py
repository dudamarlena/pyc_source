# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\type_tax.py
# Compiled at: 2013-01-23 18:09:26
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import PySide.QtCore as _qc
from banta.packages import GenericModule
import banta.utils, banta.db as _db

class TaxModel(_qc.QAbstractTableModel):
    HEADERS = (
     _qc.QT_TRANSLATE_NOOP(b'tax', b'Nombre'),
     _qc.QT_TRANSLATE_NOOP(b'tax', b'Porcentaje'))

    def __init__(self, parent=None):
        _qc.QAbstractTableModel.__init__(self, parent)
        self.parent_widget = parent
        self.tr = banta.utils.unitr(self.trUtf8)

    def rowCount(self, parent=None):
        return len(_db.DB.type_tax)

    def columnCount(self, *args, **kwargs):
        return 2

    def data(self, index, role=0):
        if not index.isValid():
            return
        else:
            if role not in (_qc.Qt.DisplayRole, _qc.Qt.EditRole):
                return
            row = index.row()
            if row >= len(_db.DB.type_tax):
                return
            col = index.column()
            tax = _db.DB.type_tax[row]
            if col == 0:
                return tax.name
            if col == 1:
                return tax.tax
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

    def insertRows(self, position, rows, index=None):
        for i in range(rows):
            self.beginInsertRows(_qc.QModelIndex(), position, position)
            tax = _db.models.TypeTax()
            _db.DB.type_tax.insert(position, tax)
            self.endInsertRows()
            position += 1

        _db.DB.commit()

    def removeRows(self, position, rows, index=None):
        self.beginRemoveRows(_qc.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            del _db.DB.type_tax[position]

        _db.DB.commit()
        self.endRemoveRows()
        return True

    def setData(self, index=None, value=None, role=0):
        if index.isValid() and role == _qc.Qt.EditRole:
            tax = _db.DB.type_tax[index.row()]
            col = index.column()
            if col == 0:
                tax.name = value
            elif col == 1:
                tax.tax = value
            _db.DB.commit()
            self.dataChanged.emit(index, index)
            return True
        return False


MODEL = TaxModel()

class TypeTax(GenericModule):

    def load(self):
        self.dialog = self.app.uiLoader.load(b':/data/ui/ttax.ui', self.app.settings.tabWidget)
        self.dialog.tr = banta.utils.unitr(self.dialog.trUtf8)
        self.app.settings.tabWidget.addTab(self.dialog, self.dialog.tr(b'Alícuotas'))
        self.model = MODEL
        self.dialog.v_ttax.setModel(self.model)
        self.dialog.bSearch.clicked.connect(self.search)
        self.dialog.bNew.clicked.connect(self.new)
        self.dialog.bDelete.clicked.connect(self.delete)

    @_qc.Slot()
    def new(self):
        self.model.insertRows(0, 1)

    @_qc.Slot()
    def search(self):
        text = self.dialog.eName.text()
        self.dialog.v_ttax.selectRow(-1)
        for i, tax in enumerate(_db.DB.type_tax):
            if text in tax.name.lower():
                self.dialog.v_ttax.selectRow(i)
                break

    @_qc.Slot()
    def delete(self):
        selected = self.dialog.v_ttax.selectedIndexes()
        if not selected:
            return
        r = selected[0].row()
        self.model.removeRows(r, 1)