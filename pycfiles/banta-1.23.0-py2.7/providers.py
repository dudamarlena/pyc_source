# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\base\providers.py
# Compiled at: 2012-10-05 10:06:42
from __future__ import absolute_import, print_function, unicode_literals
import PySide.QtCore as _qc, PySide.QtGui as _qg, banta.db as _db, banta.packages as _pack, banta.utils

class ProviderModel(_qc.QAbstractTableModel):
    HEADERS = (
     _qc.QT_TRANSLATE_NOOP(b'providers', b'Código'),
     _qc.QT_TRANSLATE_NOOP(b'providers', b'Nombre'),
     _qc.QT_TRANSLATE_NOOP(b'providers', b'Dirección'),
     _qc.QT_TRANSLATE_NOOP(b'providers', b'Teléfono'),
     _qc.QT_TRANSLATE_NOOP(b'providers', b'Correo'))
    columns = 5

    def __init__(self, parent=None):
        _qc.QAbstractTableModel.__init__(self, parent)
        self.parent_widget = parent
        self.tr = banta.utils.unitr(self.trUtf8)

    def rowCount(self, parent=None):
        return len(_db.DB.providers)

    def columnCount(self, parent=None):
        return self.columns

    def data(self, index, role=0):
        """Returns the data for an item
                The role indicates which type of data should be returned
                Accepts the UserRole because products uses this model too. so it works on findData"""
        if not index.isValid():
            return
        else:
            if role not in (_qc.Qt.DisplayRole, _qc.Qt.EditRole, _qc.Qt.UserRole):
                return
            row = index.row()
            col = index.column()
            if row >= len(_db.DB.providers):
                return
            pro = _db.DB.providers.values()[row]
            if role == _qc.Qt.UserRole or col == 0:
                return pro.code
            if col == 1:
                return pro.name
            if col == 2:
                return pro.address
            if col == 3:
                return pro.phone
            if col == 4:
                return pro.mail
            return

    def headerData(self, section=0, orientation=None, role=0):
        """Returns the data for each header"""
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
            if index.column() == 0:
                return _qc.Qt.ItemIsEnabled | _qc.Qt.ItemIsSelectable
            return _qc.Qt.ItemIsEditable | _qc.Qt.ItemIsEnabled | _qc.Qt.ItemIsSelectable
        else:
            return

    def setData(self, index=None, value=None, role=0):
        """Sets the data of a item.
                Returns True|False """
        if index.isValid() and role == _qc.Qt.EditRole:
            pro = _db.DB.providers.values()[index.row()]
            col = index.column()
            if col == 0:
                return False
            if col == 1:
                pro.name = value
            elif col == 2:
                pro.address = value
            elif col == 3:
                pro.phone = value
            elif col == 4:
                pro.mail = value
            _db.DB.commit()
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, index=None):
        for i in range(rows):
            code, ok = _qg.QInputDialog.getText(self.parent_widget, self.tr(b'Nuevo Proveedor'), self.tr(b'Ingrese el código'), _qg.QLineEdit.Normal, b'')
            if not ok:
                return False
            self.beginInsertRows(_qc.QModelIndex(), position, position)
            prov = _db.models.Provider(code)
            _db.DB.providers[prov.code] = prov
            self.endInsertRows()
            position += 1

        _db.DB.commit()
        return True

    def removeRows(self, position, rows, index=None):
        self.beginRemoveRows(_qc.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            c = _db.DB.providers.values()[position]
            del _db.DB.providers[c.code]

        _db.DB.commit()
        self.endRemoveRows()
        return True


MODEL = ProviderModel()

class Providers(_pack.GenericModule):
    REQUIRES = (
     _pack.GenericModule.P_ADMIN,)
    NAME = b'providers'

    def __init__(self, app):
        super(Providers, self).__init__(app)
        self.model = MODEL
        MODEL.parent_widget = app.window

    def load(self):
        self.app.window.vProviders.setModel(self.model)
        self.app.window.bProvNew.clicked.connect(self.new)
        self.app.window.bProvSearch.clicked.connect(self.search)
        self.app.window.bProvDelete.clicked.connect(self.delete)

    @_qc.Slot()
    def new(self):
        self.model.insertRows(0, 1)

    @_qc.Slot()
    def search(self):
        text = self.app.window.eProvName.text().lower()
        self.app.window.vProviders.selectRow(-1)
        for i, pro in enumerate(_db.DB.providers.values()):
            if text in pro.name.lower():
                self.app.window.vProviders.selectRow(i)
                break

    @_qc.Slot()
    def delete(self):
        selected = self.app.window.vProviders.selectedIndexes()
        if not selected:
            return
        r = selected[0].row()
        self.model.removeRows(r, 1)