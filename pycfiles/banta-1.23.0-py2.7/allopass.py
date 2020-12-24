# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\experimental\allopass.py
# Compiled at: 2012-10-02 15:04:52
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
from PySide import QtCore, QtGui
import banta.db, banta.db.models
from packages.generic import GenericModule

class Buys(GenericModule):
    REQUIRES = (
     GenericModule.P_ADMIN,)
    NAME = b'Buys'
    countries = ('United states', 'Chile')
    messages = b''

    def __init__(self, app):
        super(Buys, self).__init__(app)
        self.dialog = self.app.uiLoader.load(b':/data/ui/allopass.ui', self.app.window)
        self.dialog.setWindowIcon(self.app.window.windowIcon())

    def load(self):
        self.app.window.acAllopass.triggered.connect(self.code)
        self.dialog.cbCountries.setItems(self.countries)
        self.dialog.cbCountries.currentIndexChanged.connect(self.countChanged)
        self.dialog.dPacks.valueChanged.connect(self.packChanged)
        import packages.base.products
        model = self.app.modules[packages.base.products.Products.NAME].model
        cbp = self.dialog.cbProd
        cbp.setModel(model)

    @QtCore.Slot()
    def code(self):
        if self.dialog.exec_() == QtGui.QDialog.Accepted:
            pass

    @QtCore.Slot(int)
    def countChanged(self, i):
        if i < 0:
            return
        self.dialog.lb_msg.setText(self.messages[i])

    @QtCore.Slot(int)
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