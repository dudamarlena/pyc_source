# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\buys.py
# Compiled at: 2012-10-17 00:43:12
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import PySide.QtCore as _qc, PySide.QtGui as _qg, banta.packages as _pack, banta.db as _db

class Buys(_pack.GenericModule):
    REQUIRES = (
     _pack.GenericModule.P_ADMIN,)
    NAME = b'Buys'

    def __init__(self, app):
        super(Buys, self).__init__(app)
        self.app.window.bNewStockBuy.setDefaultAction(self.app.window.acNewStockBuy)
        self.dialog = self.app.uiLoader.load(b':/data/ui/buys.ui', self.app.window)
        self.dialog.setWindowIcon(self.app.window.windowIcon())

    def load(self):
        import banta.packages.base.products
        self.prod = None
        self.packs = 0
        self.pack_units = 0
        self.buy_price = 0
        self.app.window.acNewStockBuy.setEnabled(True)
        self.app.window.acNewStockBuy.triggered.connect(self.newBuy)
        self.dialog.cbProd.currentIndexChanged.connect(self.prodChanged)
        self.dialog.dPacks.valueChanged.connect(self.packChanged)
        prod_mod_name = banta.packages.base.products.Products.NAME
        model = self.app.modules[prod_mod_name].model
        cbp = self.dialog.cbProd
        cbp.setModel(model)
        return

    @_qc.Slot()
    def newBuy(self):
        if self.dialog.exec_() != _qg.QDialog.Accepted:
            return
        if not self.prod or self.units == 0:
            return
        self.prod.stock += self.units
        b = _db.models.Buy(self.prod, self.units)
        _db.DB.commit()

    @_qc.Slot(int)
    def prodChanged(self, i):
        if i < 0:
            return
        code = self.app.window.cb_billProds.itemData(i, _qc.Qt.UserRole)
        if code not in _db.DB.products:
            return
        self.prod = _db.DB.products[code]
        self.pack_units = self.prod.pack_units
        self.buy_price = self.prod.buy_price
        self.showInfo()

    @_qc.Slot(int)
    def packChanged(self, i):
        self.packs = i
        self.showInfo()

    def showInfo(self):
        self.units = self.pack_units * self.packs
        self.price = self.units * self.buy_price
        self.dialog.lb_packItems.setText(str(self.pack_units))
        self.dialog.lb_items.setText(str(self.units))
        self.dialog.lb_price.setText(str(self.buy_price))
        self.dialog.lb_total.setText(str(self.price))