# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\limits.py
# Compiled at: 2012-10-16 21:35:52
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import itertools, PySide.QtCore as _qc, PySide.QtGui as _qg, banta.utils, banta.packages as _pack, banta.db as _db

class LimitDelegate(_qg.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        self.initStyleOption(option, index)
        col = index.column()
        editor = None
        if col == 0:
            editor = _qg.QComboBox(parent)
            editor.setModel(_pack.base.products.MODEL)
            editor.setModelColumn(0)
        elif col in (1, 2):
            editor = _qg.QDoubleSpinBox(parent)
            editor.setRange(-2147483646, +2147483646)
        return editor

    def setEditorData(self, editor, index):
        col = index.column()
        d = index.data(_qc.Qt.EditRole)
        if col == 0:
            if d < 0:
                return
            i = editor.findData(d)
            if i < 0:
                return
            editor.setCurrentIndex(i)
        elif col in (1, 2):
            editor.setValue(d)
        return

    def setModelData(self, editor, model, index):
        col = index.column()
        data = None
        if col == 0:
            i = editor.currentIndex()
            data = editor.itemData(i)
        elif col in (1, 2):
            data = editor.value()
        model.setData(index, data, _qc.Qt.EditRole)
        return


class LimitModel(_qc.QAbstractTableModel):
    HEADERS = (
     _qc.QT_TRANSLATE_NOOP(b'limits', b'Producto'),
     _qc.QT_TRANSLATE_NOOP(b'limits', b'Cantidad'),
     _qc.QT_TRANSLATE_NOOP(b'limits', b'Monto'))
    columns = 3

    def __init__(self, parent=None):
        _qc.QAbstractTableModel.__init__(self, parent)
        self.parent_widget = parent
        self.tr = banta.utils.unitr(self.trUtf8)

    def rowCount(self, parent=None):
        return len(_db.DB.limits)

    def columnCount(self, parent=None):
        return self.columns

    def data(self, index, role=0):
        """Returns the data for an item
                The role indicates which type of data should be returned
                Accepts the UserRole because products uses this model too. so it works on findData"""
        if not index.isValid():
            return
        else:
            if role not in (_qc.Qt.DisplayRole, _qc.Qt.EditRole):
                return
            row = index.row()
            col = index.column()
            if row >= self.rowCount():
                return
            lim = _db.DB.limits[row]
            if col == 0:
                if lim.product is None:
                    return
                else:
                    if role == _qc.Qt.DisplayRole:
                        return lim.product.name
                    return lim.product.code

            else:
                if col == 1:
                    return lim.quantity
                if col == 2:
                    return lim.amount
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
        """Returns the flag for each item"""
        if index.isValid():
            return _qc.Qt.ItemIsEditable | _qc.Qt.ItemIsEnabled | _qc.Qt.ItemIsSelectable
        else:
            return

    def setData(self, index=None, value=None, role=0):
        """Sets the data of a item.
                Returns True|False """
        if index.isValid() and role == _qc.Qt.EditRole:
            lim = _db.DB.limits[index.row()]
            col = index.column()
            if col == 0:
                lim.product = _db.DB.products[value]
            elif col == 1:
                lim.quantity = value
            elif col == 2:
                lim.amount = value
            _db.DB.commit()
            return True
        return False

    def insertRows(self, position, rows, index=None):
        for i in range(rows):
            self.beginInsertRows(_qc.QModelIndex(), position, position)
            lim = _db.models.Limit()
            _db.DB.limits.append(lim)
            self.endInsertRows()
            position += 1

        _db.DB.commit()
        return True

    def removeRows(self, position, rows, index=None):
        self.beginRemoveRows(_qc.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            del _db.DB.limits[position]

        _db.DB.commit()
        self.endRemoveRows()
        return True


class LimitCheck:
    prod_code = None
    quantity = 0
    amount = 0

    def __init__(self, limit):
        self.prod_code = limit.product.code
        self.limit = limit

    def addQuantity(self, quant):
        if self.limit.quantity:
            self.quantity += quant
            return self.quantity <= self.limit.quantity
        return True

    def exQuantity(self):
        """Returns the remaining quantity"""
        return self.quantity - self.limit.quantity

    def addAmount(self, amount):
        if self.limit.amount:
            self.amount += amount
            return self.amount <= self.limit.amount
        return True

    def exAmount(self):
        return self.amount - self.limit.amount


class Limits(_pack.GenericModule):
    NAME = b'Limits'

    def __init__(self, app):
        super(Limits, self).__init__(app)
        self.model = LimitModel(app.window)

    def load(self):
        self.dialog = self.app.uiLoader.load(b':/data/ui/limits.ui', self.app.settings.tabWidget)
        self.dialog.tr = banta.utils.unitr(self.dialog.trUtf8)
        self.app.settings.tabWidget.addTab(self.dialog, self.dialog.tr(b'Límites'))
        self.dialog.v_limits.setModel(self.model)
        self.dialog.v_limits.setItemDelegate(LimitDelegate())
        self.dialog.bLimNew.clicked.connect(self.new)
        self.dialog.bLimDelete.clicked.connect(self.delete)
        bill_mod_name = _pack.base.bills.Bills.NAME
        self.bill_mod = self.app.modules[bill_mod_name]
        self.app.window.acBillPrint.triggered.disconnect()
        self.app.window.acBillPrint.triggered.connect(self.saveBill)

    @_qc.Slot()
    def saveBill(self):
        error_msg = self.overLimits()
        if error_msg:
            _qg.QMessageBox.critical(self.app.window, b'Banta', error_msg)
        else:
            self.bill_mod.printBill()

    def overLimits(self):
        """Checks all the limits!
                returns a string with an error message (if any)"""
        tmin, today, tmax = map(banta.utils.dateTimeToInt, banta.utils.currentMonthDates())
        checks = dict([ (lim.product.code, LimitCheck(lim)) for lim in _db.DB.limits
                      ])
        over_quant_msg = self.dialog.tr(b'Se ha excedido en la cantidad permitida para el producto código %s.' + b'\nExceso de %s unidad(es).')
        over_amount_msg = self.dialog.tr(b'Se ha excedido en el monto permitido para el producto código %s.' + b'\nExceso de $%s.')
        client = self.bill_mod.bill.client
        bills = itertools.chain([self.bill_mod.bill], _db.DB.bills.values(min=tmin, max=tmax))
        for b in bills:
            if client == b.client:
                for i in b.items:
                    lim = checks.get(i.product.code)
                    if lim:
                        if not lim.addQuantity(i.quantity):
                            return over_quant_msg % (lim.prod_code, lim.exQuantity())
                        if not lim.addAmount(i.price):
                            return over_amount_msg % (lim.prod_code, lim.exAmount())

        return

    @_qc.Slot()
    def new(self):
        self.model.insertRows(0, 1)

    @_qc.Slot()
    def delete(self):
        selected = self.dialog.v_limits.selectedIndexes()
        if not selected:
            return
        r = selected[0].row()
        self.model.removeRows(r, 1)