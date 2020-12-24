# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\base\tbill.py
# Compiled at: 2012-10-05 10:17:28
from __future__ import absolute_import, print_function, unicode_literals
import PySide.QtCore as _qc, banta.packages as _pack, banta.db.models as _mods, banta.utils

class TBillModel(_qc.QAbstractTableModel):
    HEADERS = (
     _qc.QT_TRANSLATE_NOOP(b'typebill', b'Nombre'),)

    def __init__(self, parent=None):
        _qc.QAbstractTableModel.__init__(self, parent)
        self.tr = banta.utils.unitr(self.trUtf8)

    def rowCount(self, parent=None):
        return len(_mods.Bill.TYPE_NAMES)

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role=0):
        if not index.isValid():
            return
        else:
            r = index.row()
            if r >= len(_mods.Bill.TYPE_NAMES):
                return
            if role == _qc.Qt.DisplayRole or role == _qc.Qt.EditRole:
                if index.column() == 0:
                    return _mods.Bill.TYPE_NAMES[r]
            return

    def headerData(self, section=0, orientation=None, role=0):
        if role != _qc.Qt.DisplayRole:
            return
        else:
            if orientation == _qc.Qt.Horizontal:
                return self.trUtf8(self.HEADERS[section])
            else:
                return str(section)

            return

    def flags(self, index=None):
        if index.isValid():
            return _qc.Qt.ItemIsEditable | _qc.Qt.ItemIsEnabled | _qc.Qt.ItemIsSelectable
        else:
            return


class TBill(_pack.GenericModule):
    REQUIRES = (
     _pack.GenericModule.P_ADMIN,)
    NAME = b'bill_types'

    def load(self):
        self.model = TBillModel()
        self.app.window.cb_tbill.setModel(self.model)