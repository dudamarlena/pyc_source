# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\base\users.py
# Compiled at: 2012-12-05 11:58:40
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import PySide.QtCore as _qc, PySide.QtGui as _qg, banta.packages as _pack, banta.db as _db, banta.utils

class UserModel(_qc.QAbstractTableModel):
    HEADERS = (
     _qc.QT_TRANSLATE_NOOP(b'users', b'Nombre'),
     _qc.QT_TRANSLATE_NOOP(b'users', b'Contraseña'))

    def __init__(self, parent=None):
        _qc.QAbstractTableModel.__init__(self, parent)
        self.parent_widget = parent
        self.tr = banta.utils.unitr(self.trUtf8)

    def rowCount(self, parent=None):
        return len(_db.DB.users)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=0):
        if not index.isValid():
            return
        else:
            row = index.row()
            if row >= len(_db.DB.users):
                return
            if role not in (_qc.Qt.DisplayRole, _qc.Qt.EditRole):
                return
            user = _db.DB.users[row]
            col = index.column()
            if col == 0:
                return user.name
            if col == 1:
                if role == _qc.Qt.DisplayRole:
                    return b'★★★★★'
                else:
                    return b''

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
            user = _db.DB.users[index.row()]
            col = index.column()
            if col == 0:
                user.name = value
            elif col == 1:
                value = value.strip()
                if value:
                    user.setPassword(value)
            _db.DB.commit()
            return True
        return False

    def insertRows(self, position, rows, index=None):
        for i in range(rows):
            name, ok = _qg.QInputDialog.getText(self.parent_widget, self.tr(b'Usuarios'), self.tr(b'Ingrese el nombre del usuario'), _qg.QLineEdit.Normal, b'')
            if not ok:
                return False
            self.beginInsertRows(_qc.QModelIndex(), position, position)
            user = _db.models.User(name)
            _db.DB.users.insert(position, user)
            self.endInsertRows()
            position += 1

        _db.DB.commit()

    def removeRows(self, position, rows, index=None):
        self.beginRemoveRows(_qc.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            _db.DB.users.pop(position)

        _db.DB.commit()
        self.endRemoveRows()
        return True


class Users(_pack.GenericModule):
    REQUIRES = (
     _pack.GenericModule.P_ADMIN,)
    NAME = b'users'

    def __init__(self, app):
        super(Users, self).__init__(app)
        self.model = UserModel(self.app.window)
        self.app.window.cb_billUser.setEnabled(False)
        self.app.window.cb_billUser.setModel(self.model)

    def load(self):
        self.dialog = self.app.uiLoader.load(b':/data/ui/users.ui')
        self.dialog.tr = banta.utils.unitr(self.dialog.trUtf8)
        self.app.settings.tabWidget.addTab(self.dialog, self.dialog.tr(b'Usuarios'))
        self.dialog.v_users.setModel(self.model)
        self.app.window.cb_billUser.setEnabled(True)
        self.dialog.bUNew.clicked.connect(self.new)
        self.dialog.bUSearch.clicked.connect(self.search)
        self.dialog.bUDelete.clicked.connect(self.delete)

    @_qc.Slot()
    def new(self):
        self.model.insertRows(0, 1)

    @_qc.Slot()
    def search(self):
        text = self.dialog.eUName.text()
        self.dialog.v_users.selectRow(-1)
        for i, user in enumerate(_db.DB.users):
            if text in user.name.lower():
                self.dialog.v_users.selectRow(i)
                break

    @_qc.Slot()
    def delete(self):
        selected = self.dialog.v_users.selectedIndexes()
        if not selected:
            return
        r = selected[0].row()
        self.model.removeRows(r, 1)