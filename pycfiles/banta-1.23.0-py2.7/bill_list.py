# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\bill_list.py
# Compiled at: 2013-01-28 20:29:48
""" Module for listing bills
"""
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import datetime, csv, banta.packages as _pack, PySide.QtCore as _qc, PySide.QtGui as _qg, banta.db as _db, banta.utils
REQUIRES = list()
LICENSES = ()

class BillList(_pack.GenericModule):
    REQUIRES = (
     _pack.GenericModule.P_ADMIN,)
    NAME = b'bill list'

    def __init__(self, app):
        super(BillList, self).__init__(app)

    def load(self):
        self.widget = self.app.uiLoader.load(b':/data/ui/bill_list.ui')
        self.app.window.tabWidget.addTab(self.widget, self.app.window.tr(b'Lista de Facturas'))
        month_start, today, month_end = banta.utils.currentMonthDates()
        self.widget.dBListMin.setDate(month_start)
        self.widget.dBListMax.setDate(month_end)
        self.widget.bBListShow.clicked.connect(self.show)
        self.widget.bExportDraft.clicked.connect(self.exportDrafts)
        self.widget.tBList.doubleClicked.connect(self.showBill)

    @_qc.Slot()
    def exportDrafts(self):
        """Exports DRAFTS from the bill list, also deleting them"""
        _db.DB.commit()
        name = b'banta_bills-' + str(datetime.datetime.now()).replace(b':', b'_') + b'.csv'
        delimit = (b';').encode(b'utf-8')
        quote = (b'"').encode(b'utf-8')
        writer = csv.writer(open(name, b'wb'), delimiter=delimit, quotechar=quote, quoting=csv.QUOTE_MINIMAL)
        ret = _qg.QMessageBox.question(self.app.window, self.app.window.tr(b'Banta - Exportar'), self.app.window.tr(b'¿Desea eliminar los presupuestos?'), _qg.QMessageBox.Yes | _qg.QMessageBox.No, _qg.QMessageBox.No)
        delete = ret == _qg.QMessageBox.Yes
        tmin, tmax = banta.utils.getTimesFromFilters(self.widget.dBListMin, self.widget.dBListMax)
        row = []
        for c in range(self.widget.tBList.columnCount()):
            hi = self.widget.tBList.horizontalHeaderItem(c)
            row.append(hi.text().encode(b'utf-8'))

        try:
            writer.writerow(row)
        except:
            pass

        to_delete = []
        for bill in _db.DB.bills.values(min=tmin, max=tmax):
            d = (
             bill.time, bill.number, bill.date, bill.TYPE_NAMES[bill.btype].encode(b'utf-8', b'replace'),
             bill.client.name.encode(b'utf-8', b'replace'), bill.tax, bill.total, len(bill.items), bill.strPrinted(),
             bill.user and bill.user.name.encode(b'utf-8', b'replace'))
            try:
                writer.writerow(d)
                if delete and not bill.printed:
                    to_delete.append(bill.time)
            except:
                pass

        for k in to_delete:
            del _db.DB.bills[k]

        if to_delete:
            _db.DB.commit(b'system', b'drafts exported and purged')
        logger.info(b'Draft exported correctly, %s registries deleted from db' % len(to_delete))

    @_qc.Slot()
    def show(self):
        tb = self.widget.tBList
        tb.setRowCount(0)
        total = 0.0
        tax_total = 0.0
        tmin, tmax = banta.utils.getTimesFromFilters(self.widget.dBListMin, self.widget.dBListMax)
        for b in _db.DB.bills.values(min=tmin, max=tmax):
            r = tb.rowCount()
            tb.setRowCount(r + 1)
            total += b.total
            tax_total += b.tax
            texts = (
             str(b.time), str(b.number), _qc.QDateTime(b.date).toString(), b.TYPE_NAMES[b.btype],
             b.client.name, str(b.tax), str(b.total), str(len(b.items)),
             b.strPrinted(), b.user and b.user.name)
            for c, t in enumerate(texts):
                tb.setItem(r, c, _qg.QTableWidgetItem(t))

        self.app.window.statusbar.showMessage(b'Total $%s (IVA %s)' % (total, tax_total))

    @_qc.Slot(_qc.QModelIndex)
    def showBill(self, mi):
        row = mi.row()
        code = int(self.widget.tBList.item(row, 0).text())
        b = _db.DB.bills[code].copy()
        self.app.modules[b'bills'].showBill(b)