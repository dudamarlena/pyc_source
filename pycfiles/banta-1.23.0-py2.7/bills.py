# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\base\bills.py
# Compiled at: 2013-02-01 14:52:56
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import PySide.QtCore as _qc, PySide.QtGui as _qg, banta.db as _db, banta.packages as _pkg, banta.utils

class Bills(_qc.QObject, _pkg.GenericModule):
    REQUIRES = (
     _pkg.GenericModule.P_SELL,)
    NAME = b'bills'
    startPrinting = _qc.Signal(object)
    startPrintingDraft = _qc.Signal(object)

    def __init__(self, app, *args, **kwargs):
        super(Bills, self).__init__()
        self.app = app
        self.bill = None
        self.item = None
        return

    def load(self):
        w = self.app.window
        w.acItemAdd.triggered.connect(self.itemAdd)
        w.acItemDelete.triggered.connect(self.itemDelete)
        w.acBillNew.triggered.connect(self.new)
        w.acBillPrint.triggered.connect(self.printBill)
        w.acSaveDraft.triggered.connect(self.printDraft)
        w.acChangeClientSearch.triggered.connect(self.changeClientSearch)
        w.bBillAdd.setDefaultAction(w.acItemAdd)
        w.bBillNew.setDefaultAction(w.acBillNew)
        w.bBillDelete.setDefaultAction(w.acItemDelete)
        w.bBillPrint.setDefaultAction(w.acBillPrint)
        w.bDraft.setDefaultAction(w.acSaveDraft)
        w.bChangeType.setDefaultAction(w.acChangeClientSearch)
        w.cb_tbill.currentIndexChanged.connect(self.typeChanged)
        w.cb_tpay.currentIndexChanged.connect(self.payChanged)
        w.cb_billProds.currentIndexChanged.connect(self.prodChanged)
        w.cb_clients.currentIndexChanged.connect(self.clientChanged)
        w.cb_billUser.currentIndexChanged.connect(self.userChanged)
        w.eProdDetail.editingFinished.connect(self.prodDetailChanged)
        w.cb_billIva.setModel(_pkg.optional.type_tax.MODEL)
        w.cb_billIva.currentIndexChanged.connect(self.taxChanged)
        w.cb_clients.editTextChanged.connect(w.lBCliDetail.clear)
        w.cb_billProds.lineEdit().returnPressed.connect(self.itemAdd)
        w.eProdDetail.returnPressed.connect(self.itemAdd)
        v = _qg.QTableView()
        v.setSelectionMode(_qg.QTableView.SingleSelection)
        v.setSelectionBehavior(_qg.QTableView.SelectRows)
        w.cb_clients.setView(v)
        for c in (2, 4, 5, 6):
            v.setColumnHidden(c, True)

        w.cb_clients.setModelColumn(1)
        w.eBProdQuant.valueChanged.connect(self.prodQuantChanged)
        w.dsPrice.valueChanged.connect(self.priceChanged)
        w.acBillNew.trigger()
        self.loadNewClientDialog()

    def loadNewClientDialog(self):
        self.dialog = self.app.uiLoader.load(b':/data/ui/temp_client.ui', self.app.window)
        self.dialog.tr = banta.utils.unitr(self.dialog.trUtf8)
        self.dialog.setWindowIcon(self.app.window.windowIcon())
        self.dialog.setWindowTitle(self.dialog.tr(b'Nuevo cliente casual'))
        self.app.window.bNewCasualClient.setDefaultAction(self.app.window.acNewCasualClient)
        self.app.window.acNewCasualClient.triggered.connect(self.newCasualClient)
        self.dialog.cbTaxType.addItems(_db.models.Client.TAX_NAMES)
        self.dialog.cbCodeType.addItems(_db.models.Client.DOC_NAMES)
        self.dialog.cbIBType.addItems(_db.models.Client.IB_NAMES)

    @_qc.Slot(float)
    def priceChanged(self, value):
        """When the price changes, set the price to the current item."""
        self.item.base_price = value
        self.updateItem()

    @_qc.Slot()
    def prodDetailChanged(self):
        if not self.item:
            return
        text = self.app.window.eProdDetail.text()
        self.item.description = text

    @_qc.Slot(int)
    def userChanged(self, i):
        """Called when the user of a bill changes"""
        if i == -1:
            return
        self.bill.user = _db.DB.users[i]

    @_qc.Slot(int)
    def clientChanged(self, i):
        """Called when the client is changed on the cb"""
        if i == -1:
            return
        code = self.app.window.cb_clients.itemData(i, _qc.Qt.UserRole)
        client = _db.DB.clients[code]
        self.setClient(client)

    @_qc.Slot()
    def changeClientSearch(self):
        col = self.app.window.cb_clients.modelColumn()
        if col == 1:
            col = 0
            text = self.app.window.tr(b'Código del cliente')
        else:
            col = 1
            text = self.app.window.tr(b'Nombre del cliente')
        self.app.window.cb_clients.setModelColumn(col)
        self.app.window.lBClient.setText(text)

    @_qc.Slot()
    def printDraft(self):
        ret = self._askToPrint(True)
        if ret == _qg.QMessageBox.Cancel:
            return
        if ret == _qg.QMessageBox.Yes:
            self.bill.calculate()
            self.startPrintingDraft.emit(self.bill)
            self.app.window.acBillNew.trigger()
        else:
            self.onPrintingFinish((True, self.bill, -1, b''))

    @_qc.Slot()
    def printBill(self):
        if self._askToPrint(False) == _qg.QMessageBox.Yes:
            if self.bill.printed:
                _qg.QMessageBox.information(self.app.window, self.app.window.tr(b'Banta - Imprimir'), self.app.window.tr(b'Esta factura ya ha sido impresa.'))
                return False
            self.bill.calculate()
            self.startPrinting.emit(self.bill)
            self.app.window.acBillNew.trigger()

    def _askToPrint(self, draft=False):
        if not self.bill.client:
            _qg.QMessageBox.information(self.app.window, self.app.window.tr(b'Banta - Imprimir'), self.app.window.tr(b'No se ha indicado el cliente'))
            return _qg.QMessageBox.Cancel
        options = _qg.QMessageBox.Yes | _qg.QMessageBox.Cancel
        if draft:
            options |= _qg.QMessageBox.No
        msgBox = _qg.QMessageBox(_qg.QMessageBox.Question, self.app.window.tr(b'Banta - Imprimir'), self.app.window.tr(b'¿Desea imprimir?'), options, self.app.window)
        msgBox.setDefaultButton(_qg.QMessageBox.Cancel)
        self.app.dialog = msgBox
        ret = self.app.dialog.exec_()
        return ret

    @_qc.Slot(list)
    def onPrintingFinish(self, result):
        """slot for when the printer finishes printing something,
                returns a tuple with the information
                 types: (bool, _db.models.bill, int)
                        values: (success, original bill object, bill number(if <0 then is a draft), error string (if any))
                """
        if len(result) != 4:
            return
        success, bill, number, error = result
        if success:
            if number >= 0:
                bill.number = number
                bill.printed = True
            bill.close()
            _db.DB.commit()
            if bill == self.bill:
                self.app.window.acBillNew.trigger()
        else:
            msg = str(error).decode(b'utf-8', b'ignore')
            msg = self.app.window.tr(b'No se ha podido realizar la impresión\n{0}\n¿Desea volver a editar la factura?\nSi elige NO, la factura NO se guardará.').format(msg)
            logger.error(msg)
            ret = _qg.QMessageBox.question(self.app.window, self.app.window.tr(b'Impresión Fallida '), msg, _qg.QMessageBox.Yes | _qg.QMessageBox.No, _qg.QMessageBox.Yes)
            if ret == _qg.QMessageBox.Yes:
                self.showBill(bill)

    @_qc.Slot(int)
    def typeChanged(self, i):
        if i < 0:
            self.bill.tax = 0.0
            self.bill.number = 0
        else:
            self.bill.setTypeBill(i)
        self.showInfo()

    @_qc.Slot(int)
    def payChanged(self, i):
        if i < 0:
            return
        tp = _db.DB.typePays[i]
        self.bill.setTypePay(tp)
        self.item.markup = self.bill.markup
        self.updateAllItems()
        self.showInfo()
        self.updateItem()

    @_qc.Slot(int)
    def prodChanged(self, i):
        if i == -1:
            self.app.window.dsPrice.setValue(0.0)
            self.app.window.eBProdQuant.setValue(0.0)
            self.app.window.eProdDetail.setText(b'')
            self.app.window.cb_billIva.setCurrentIndex(0)
            return
        code = self.app.window.cb_billProds.itemData(i, _qc.Qt.UserRole)
        prod = _db.DB.products[code]
        self.item.setProduct(prod)
        self.app.window.dsPrice.setValue(prod.price)
        self.app.window.eProdDetail.setText(self.item.description)
        try:
            tax_index = _db.DB.type_tax.index(prod.tax_type)
        except:
            tax_index = 0

        self.app.window.cb_billIva.setCurrentIndex(tax_index)
        self.updateItem()

    @_qc.Slot(float)
    def prodQuantChanged(self, quant):
        self.item.setQuantity(quant)

    @_qc.Slot(int)
    def taxChanged(self, val):
        if val < 0:
            return
        self.item.tax_type = _db.DB.type_tax[val]
        self.updateItem()

    @_qc.Slot()
    def itemAdd(self):
        """Adds an item to the current bill. And does      all the critical logic related to it"""
        self.app.window.eBProdQuant.setFocus()
        if self.item.product is None:
            self.app.window.statusbar.showMessage(self.app.window.tr(b'Debe seleccionar un producto.'))
            return
        else:
            if self.bill.addItem(self.item):
                r = self.app.window.tb_bill.rowCount()
                self.app.window.tb_bill.setRowCount(r + 1)
                i = self.item
                i.calculate()
                texts = (
                 i.product.code, i.description, str(i.base_price), str(i.quantity),
                 str(i.markup), str(i.net_price), str(i.tax_total), str(i.price))
                for c, t in enumerate(texts):
                    self.app.window.tb_bill.setItem(r, c, _qg.QTableWidgetItem(t))

            self.item = _db.models.Item(markup=self.bill.markup)
            self.app.window.cb_billProds.setCurrentIndex(-1)
            self.app.window.eBProdQuant.setValue(1)
            self.app.window.dsPrice.setValue(0.0)
            self.updateItem()
            self.showInfo()
            return

    @_qc.Slot()
    def itemDelete(self):
        """Removes an item from the bill"""
        r = self.app.window.tb_bill.currentRow()
        if r < 0:
            return
        self.bill.delItem(r)
        self.app.window.tb_bill.removeRow(r)
        self.showInfo()

    @_qc.Slot()
    def new(self):
        """Creates a new BILL"""
        self.bill = _db.models.Bill()
        if not self.item:
            self.item = _db.models.Item()
        self.app.window.tb_bill.setRowCount(0)
        self.app.window.cb_tbill.setCurrentIndex(-1)
        self.app.window.cb_clients.setCurrentIndex(-1)
        self.app.window.cb_tpay.setCurrentIndex(0)
        self.app.window.cb_billProds.setCurrentIndex(-1)
        self.app.window.lBCliDetail.setText(b'')
        self.app.window.cb_billUser.currentIndexChanged.emit(self.app.window.cb_billUser.currentIndex())
        self.app.window.cb_tpay.currentIndexChanged.emit(0)
        self.showInfo()

    @_qc.Slot()
    def newCasualClient(self):
        """Creates a new Client for a temporary use (one shot/one buy)
                The idea of this is not to bloat the client list with one-time shoppers
                """
        d = self.dialog
        d.eName.setText(b'')
        d.eCode.setText(b'')
        d.eAddress.setText(b'')
        d.cbCodeType.setCurrentIndex(_db.models.Client.DOC_DNI)
        d.cbTaxType.setCurrentIndex(_db.models.Client.TAX_CONSUMIDOR_FINAL)
        d.cbIBType.setCurrentIndex(_db.models.Client.IB_UNREGISTERED)
        if d.exec_() != _qg.QDialog.Accepted:
            return
        name = d.eName.text()
        code = d.eCode.text()
        address = d.eAddress.text()
        t_code = d.cbCodeType.currentIndex()
        t_tax = d.cbTaxType.currentIndex()
        t_ib = d.cbIBType.currentIndex()
        c = _db.models.Client(code, name, address, t_code, t_tax, t_ib, save=False)
        self.setClient(c)

    def showInfo(self):
        """Updates the info for the bill"""
        self.bill.calculate()
        w = self.app.window
        w.lBillSubtotalA.setText(str(self.bill.subtotal))
        w.lBillTax.setText(str(self.bill.tax))
        w.lBillTotal.setText(str(self.bill.total))
        w.lBillNumber.setText(str(self.bill.number))

    def updateItem(self):
        """Updates the info for the current item"""
        self.item.calculate()
        p = self.item.price
        self.app.window.lBItemTotal.setText(str(p))

    def updateAllItems(self):
        """Updates the info for the items added to the bill. mostly affected by stuff like TypePay change and Client change..
                (notice that the "current" item is not updated, for that, use updateItem)
                recalculate indicates when is needed to recalculate the items.
                 Normally is false when we are reloading a saved bill
                """
        self.app.window.tb_bill.setRowCount(len(self.bill.items))
        for r, i in enumerate(self.bill.items):
            if not self.bill.printed:
                i.calculate()
            texts = (i.product.code, i.description, str(i.base_price), str(i.quantity),
             str(i.markup), str(i.net_price), str(i.tax_total), str(i.price))
            for c, t in enumerate(texts):
                self.app.window.tb_bill.setItem(r, c, _qg.QTableWidgetItem(t))

    def showBill(self, bill):
        """This function sets a bill as the current, and loads all its info.
                Used from bill_list
                bill param is a bill object from the database or _db.models.Bill
                """
        self.bill = bill
        self.app.window.cb_tbill.setCurrentIndex(self.bill.btype)
        if self.bill.ptype is not None:
            tp = self.app.window.cb_tpay
            i = tp.findText(self.bill.ptype.name)
            if i > -1:
                tp.setCurrentIndex(i)
        else:
            print(self.bill.ptype)
            print(b'NO PAYMENT TYPE SET!')
        cb = self.app.window.cb_clients
        code = bill.client.code
        i = cb.findData(code)
        if i > -1:
            cb.setCurrentIndex(i)
        self.app.window.tabWidget.setCurrentIndex(0)
        self.showInfo()
        self.updateAllItems()
        return

    def setClient(self, client):
        """Sets a client to the current bill"""
        _info = b'The client can be a existing client in the database or a new one\n\t\tLook at the beauty of zodb, we can assign a new instance without having to\n\t\tput it on the clients tree. Using a correct logic in the code this will\n\t\tmake everything run as expected without any drawback.\n\t\t'
        if not self.bill:
            return
        self.bill.setClient(client)
        d = (client.code, client.name, client.taxStr())
        self.app.window.lBCliDetail.setText(b'[%s] %s (%s)' % d)
        bill_types = client.getPossibleBillTypes()
        cbt = self.app.window.cb_tbill.currentIndex()
        if cbt not in bill_types:
            self.app.window.cb_tbill.setCurrentIndex(bill_types[0])
        client_exempt = client.tax_type == client.TAX_EXENTO
        self.item.client_exempt = client_exempt
        for i, item in enumerate(self.bill.items):
            item.client_exempt = client_exempt

        self.updateItem()
        self.updateAllItems()