# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\base\clients.py
# Compiled at: 2013-01-09 09:39:56
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import PySide.QtCore as _qc, PySide.QtGui as _qg, banta.utils, banta.db as _db, banta.packages as _pkg

class ClientDelegate(_qg.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        self.initStyleOption(option, index)
        col = index.column()
        editor = None
        if col in (0, 1, 2):
            editor = _qg.QLineEdit(parent)
        elif col == 3:
            editor = _qg.QComboBox(parent)
            editor.addItems(_db.models.Client.TAX_NAMES)
        elif col == 4:
            editor = _qg.QComboBox(parent)
            editor.addItems(_db.models.Client.DOC_NAMES)
        elif col == 5:
            editor = _qg.QComboBox(parent)
            editor.addItems(_db.models.Client.IB_NAMES)
        elif col == 6:
            editor = _qg.QDoubleSpinBox(parent)
            editor.setRange(-2147483646, +2147483646)
        return editor

    def setEditorData(self, editor, index):
        col = index.column()
        d = index.data(_qc.Qt.EditRole)
        if col in (0, 1, 2):
            editor.setText(d)
        elif col in (3, 4, 5):
            editor.setCurrentIndex(d)
        elif col == 6:
            editor.setValue(d)

    def setModelData(self, editor, model, index):
        col = index.column()
        data = None
        if col in (0, 1, 2):
            data = editor.text()
        elif col in (3, 4, 5):
            data = editor.currentIndex()
        elif col == 6:
            data = editor.value()
        model.setData(index, data, _qc.Qt.EditRole)
        return


class ClientModel(_qc.QAbstractTableModel):
    HEADERS = (
     _qc.QT_TRANSLATE_NOOP(b'clients', b'DNI/CUIT/CUIL'),
     _qc.QT_TRANSLATE_NOOP(b'clients', b'Nombre'),
     _qc.QT_TRANSLATE_NOOP(b'clients', b'Dirección'),
     _qc.QT_TRANSLATE_NOOP(b'clients', b'Tipo Iva'),
     _qc.QT_TRANSLATE_NOOP(b'clients', b'Tipo Documento'),
     _qc.QT_TRANSLATE_NOOP(b'clients', b'Ingresos Brutos'),
     _qc.QT_TRANSLATE_NOOP(b'clients', b'Saldo'))
    max_rows = 0

    def __init__(self, parent=None):
        _qc.QAbstractTableModel.__init__(self, parent)
        self.parent_widget = parent
        self.tr = banta.utils.unitr(self.trUtf8)
        self._setMaxRows()

    def _setMaxRows(self):
        """Sets the rowcount in the model depending on the license, clamping if the actual rowcount is larger
                that way the data is preserved when the license expires
                Is Important to call this function when the quantity of products changes
                (in theory that's well managed using this model for adding/removing rows)
                """
        self.max_rows = len(_db.DB.clients)

    def rowCount(self, parent=None):
        return self.max_rows

    def columnCount(self, parent=None):
        return 7

    def index(self, row, col, parent=None):
        """Creates an index for someone OUTSIDE the model with improved speed"""
        if row < 0 or col < 0 or row >= self.max_rows:
            return self.createIndex(row, col)
        else:
            pro = _db.DB.clients.values()[row]
            return self.createIndex(row, col, pro)

    def data(self, index, role=0):
        if not index.isValid():
            return
        if role not in (_qc.Qt.DisplayRole, _qc.Qt.EditRole, _qc.Qt.UserRole):
            return
        else:
            cli = index.internalPointer()
            if role == _qc.Qt.UserRole:
                return cli.idn
            col = index.column()
            if role == _qc.Qt.DisplayRole:
                if col == 0:
                    return cli.code
                else:
                    if col == 1:
                        return cli.name
                    if col == 2:
                        return cli.address
                    if col == 3:
                        return cli.taxStr()
                    if col == 4:
                        return cli.docStr()
                    if col == 5:
                        return cli.IBStr()
                    if col == 6:
                        return cli.balance
                    return

            elif role == _qc.Qt.EditRole:
                if col == 0:
                    return cli.code
                if col == 1:
                    return cli.name
                if col == 2:
                    return cli.address
                if col == 3:
                    return cli.tax_type
                if col == 4:
                    return cli.doc_type
                if col == 5:
                    return cli.ib_type
                if col == 6:
                    return cli.balance
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
            cli = index.internalPointer()
            col = index.column()
            if col == 0:
                cli.code = value
            elif col == 1:
                cli.setName(value)
            elif col == 2:
                cli.setAddress(value)
            elif col == 3:
                cli.tax_type = value
            elif col == 4:
                cli.doc_type = value
            elif col == 5:
                cli.ib_type = value
            elif col == 6:
                cli.balance = value
            _db.DB.commit()
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, index=None):
        for i in range(rows):
            endpos = len(_db.DB.clients)
            self.beginInsertRows(_qc.QModelIndex(), endpos, endpos)
            cli = _db.models.Client(b'', self.tr(b'Nuevo cliente'))
            self._setMaxRows()
            self.endInsertRows()
            position += 1

        _db.DB.commit()
        return True

    def removeRows(self, position, rows, index=None):
        self.beginRemoveRows(_qc.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            c = _db.DB.clients.values()[position]
            del _db.DB.clients[c.idn]

        _db.DB.commit()
        self._setMaxRows()
        self.endRemoveRows()
        return True

    def endResetModel(self, *args, **kwargs):
        self._setMaxRows()
        _qc.QAbstractTableModel.endResetModel(self, *args, **kwargs)


class Clients(_pkg.GenericModule):
    REQUIRES = (
     _pkg.GenericModule.P_ADMIN,)
    NAME = b'clients'

    def __init__(self, app):
        super(Clients, self).__init__(app)
        self.model = ClientModel(self.app.window)
        self.app.window.cb_clients.setModel(self.model)
        self.proxy_model = _qg.QSortFilterProxyModel(self.app.window.v_clients)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(1)
        self.proxy_model.setFilterCaseSensitivity(_qc.Qt.CaseInsensitive)
        self.proxy_model.rowsInserted.connect(self.rowInserted, _qc.Qt.QueuedConnection)
        self.app.window.v_clients.setModel(self.proxy_model)
        delegate = ClientDelegate(self.app.window)
        self.app.window.v_clients.setItemDelegate(delegate)
        self.app.window.bCliNew.clicked.connect(self.new)
        self.app.window.bCliDelete.clicked.connect(self.delete)
        self.app.window.eCliCode.textChanged.connect(self.proxy_model.setFilterWildcard)

    @_qc.Slot()
    def new(self):
        self.model.insertRows(0, 1)

    @_qc.Slot(_qc.QModelIndex, int, int)
    def rowInserted(self, parent, start, end):
        """This slot gets called when a row is inserted (read new) when a row is inserted, we dont actually know where
                 it gets inserted because keys are sorted, and key bounds position """
        self.app.window.v_clients.selectRow(start)
        sel = self.app.window.v_clients.selectedIndexes()
        if sel:
            i = sel[0]
            self.app.window.v_clients.scrollTo(i, _qg.QTableView.EnsureVisible)

    @_qc.Slot()
    def delete(self):
        selected = self.app.window.v_clients.selectedIndexes()
        if not selected:
            return
        r = selected[0].row()
        self.proxy_model.removeRows(r, 1)