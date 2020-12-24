# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\reports.py
# Compiled at: 2012-12-05 19:34:34
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import csv, datetime, PySide.QtCore as _qc, PySide.QtGui as _qg, banta.packages as _packs, banta.utils as _utils, banta.db as _db

class ResultProduct:
    code = b''
    name = b''
    count = 0
    total_sold = 0.0

    def __lt__(self, other):
        return self.total_sold < other.total_sold

    def toList(self):
        return (
         self.name, self.total_sold)

    def toStringList(self):
        return (
         self.code, self.name, str(self.count), str(self.total_sold))


class ResultCategory:
    prod_count = 0
    total_sold = 0.0
    total_tax = 0.0
    name = b''

    def toList(self):
        return (self.name, self.total_sold)

    def __lt__(self, other):
        return self.total_sold < other.total_sold

    def toStringList(self):
        return (
         self.name, str(self.prod_count), str(self.total_sold), str(self.total_tax))


class ResultUser:
    name = b''
    count = 0
    prod_count = 0
    total_sold = 0.0

    def __lt__(self, other):
        return self.total_sold < other.total_sold

    def toList(self):
        return (
         self.name, self.total_sold)

    def toStringList(self):
        return (
         self.name, str(self.count), str(self.prod_count), str(self.total_sold))


class ResultClient:
    code = b''
    ctype = b''
    name = b''
    count = 0
    prod_count = 0
    total_bought = 0.0

    def __lt__(self, other):
        return self.total_bought < other.total_bought

    def toList(self):
        return (
         self.name, self.total_bought)

    def toStringList(self):
        return (
         str(self.code), str(self.ctype), self.name, str(self.count), str(self.prod_count), str(self.total_bought))


class ResultMove:
    date = b''
    code = b''
    name = b''
    diff = 0
    reason = b''

    def __lt__(self, other):
        return self.diff < other.diff

    def toList(self):
        return (
         self.name, self.diff)

    def toStringList(self):
        return (
         _qc.QDateTime(self.date).toString(), self.code, self.name, str(self.diff), self.reason)


class ResultBuy:
    date = 0
    prod_code = b''
    prod_name = b''
    quantity = 0.0
    total = 0.0

    def __lt__(self, other):
        return self.total < other.total

    def toList(self):
        return (
         self.prod_name, self.total)

    def toStringList(self):
        return (
         _qc.QDateTime(self.date).toString(), self.prod_code, self.prod_name, unicode(self.quantity), unicode(self.total))


def reportBuy(times, root):
    results = {b'_headers': ('Fecha', 'Código', 'Producto', 'Cantidad', 'Total'), 
       b'_idx_tag': 2, 
       b'_idx_val': 4}
    tmin, tmax = times
    try:
        for m in _db.DB.buys.values(min=tmin, max=tmax):
            r = ResultBuy()
            r.date = m.date
            r.prod_code = m.product.code
            r.prod_name = m.product.name
            r.quantity = m.quantity
            r.total = m.total
            results[r.date] = r

    except Exception as e:
        logger.exception(b'Error when generating the report\n' + str(e))

    return results


def reportMove(times, root):
    results = {b'_headers': ('Fecha', 'Código', 'Producto', 'Diferencia', 'Razón'), 
       b'_idx_tag': 2, 
       b'_idx_val': 3}
    tmin, tmax = times
    try:
        moves = root[b'moves']
        for m in moves.values(min=tmin, max=tmax):
            r = ResultMove()
            r.date = m.date
            r.code = m.product.code
            r.name = m.product.name
            r.diff = m.diff
            r.reason = m.reason
            results[r.date] = r

    except Exception as e:
        logger.exception(b'Error when generating the report\n' + str(e))

    return results


def reportClient(times, root=None):
    results = {b'_headers': ('Código', 'Tipo', 'Nombre', 'Compras', 'Items', 'Total Comprado'), 
       b'_idx_tag': 2, 
       b'_idx_val': 5}
    tmin, tmax = times
    try:
        bills = root[b'bills']
        for b in bills.values(min=tmin, max=tmax):
            cli = b.client
            if not cli:
                continue
            ccode = cli.code
            if ccode in results:
                res = results[ccode]
            else:
                res = ResultClient()
                res.code = ccode
                res.name = cli.name
                res.ctype = cli.DOC_NAMES[cli.doc_type]
                results[ccode] = res
            res.count += 1
            res.prod_count += sum([ i.quantity for i in b.items ])
            res.total_bought += b.total

    except Exception as e:
        logger.exception(b'Error when generating the report\n' + str(e))

    return results


def reportUser(times, root):
    results = {b'_headers': ('Usuario', 'Facturas', 'Productos', 'Total Vendido'), 
       b'_idx_tag': 0, 
       b'_idx_val': 3}
    tmin, tmax = times
    bills = root[b'bills']
    try:
        for b in bills.values(min=tmin, max=tmax):
            user = b.user
            if not user:
                uname = b'No especificado'
            else:
                uname = user.name
            if uname not in results:
                res = ResultUser()
                res.name = uname
                results[uname] = res
            r = results[uname]
            r.count += 1
            r.prod_count += sum([ i.quantity for i in b.items ])
            r.total_sold += b.total

    except Exception as e:
        logger.exception(b'Error when generating the report\n' + str(e))

    return results


def reportCategory(times, root):
    results = {b'_headers': ('Rubro', 'Productos', 'Total Vendido', 'Impuesto'), 
       b'_idx_tag': 0, 
       b'_idx_val': 2}
    tmin, tmax = times
    bills = root[b'bills']
    try:
        for b in bills.values(min=tmin, max=tmax):
            for i in b.items:
                cat = i.product.category
                if not cat:
                    cname = b'Sin rubro'
                else:
                    cname = cat.name
                if cname not in results:
                    res = ResultCategory()
                    res.name = cname
                    results[cname] = res
                r = results[cname]
                r.prod_count += i.quantity
                r.total_sold += i.price
                r.total_tax += i.tax_total

    except Exception as e:
        logger.exception(b'Error when generating the report\n' + str(e))

    return results


def reportProduct(times, root):
    """Calculates a report of products and returns a list of results
        times is a tuple with the min and max time (as int objects) (utils.dateTimeToInt)
        root is the root of the database, this is needed so this report can be generated from several threads
        """
    tmin, tmax = times
    results = {b'_headers': ('Código', 'Nombre', 'Cantidad', 'Total Vendido'), 
       b'_idx_tag': 1, 
       b'_idx_val': 3}
    bills = root[b'bills']
    try:
        for b in bills.values(min=tmin, max=tmax):
            for i in b.items:
                prod = i.product
                if not prod:
                    continue
                pcode = prod.code
                if pcode not in results:
                    res = ResultProduct()
                    res.name = prod.name
                    res.code = pcode
                    results[pcode] = res
                r = results[pcode]
                r.count += i.quantity
                r.total_sold += i.price

    except Exception as e:
        logger.exception(b'Error when generating the report\n' + str(e))

    return results


class Reports(_packs.GenericModule):
    REQUIRES = (
     _packs.GenericModule.P_ADMIN,)
    NAME = b'reports'
    REPORT_NAMES = (
     _qc.QT_TRANSLATE_NOOP(b'reports', b'Por Rubro'),
     _qc.QT_TRANSLATE_NOOP(b'reports', b'Por Producto'),
     _qc.QT_TRANSLATE_NOOP(b'reports', b'Por Usuario'),
     _qc.QT_TRANSLATE_NOOP(b'reports', b'Por Cliente'),
     _qc.QT_TRANSLATE_NOOP(b'reports', b'Movimientos'),
     _qc.QT_TRANSLATE_NOOP(b'reports', b'Compras'))

    def load(self):
        self.REPORT_FUNCS = (
         reportCategory,
         reportProduct,
         reportUser,
         reportClient,
         reportMove,
         reportBuy)
        self.widget = self.app.uiLoader.load(b':/data/ui/reports.ui')
        self.widget.tr = _utils.unitr(self.widget.trUtf8)
        self.app.window.tabWidget.addTab(self.widget, self.widget.tr(b'Reportes'))
        month_start, today, month_end = _utils.currentMonthDates()
        self.widget.dMin.setDate(month_start)
        self.widget.dMax.setDate(month_end)
        self.widget.cb_type.addItems(self.REPORT_NAMES)
        self.widget.bShow.clicked.connect(self.show)
        self.widget.bExport.clicked.connect(self.export)

    @_qc.Slot()
    def show(self):
        rep_type = self.widget.cb_type.currentIndex()
        if rep_type < 0:
            return
        self.widget.v_list.clear()
        times = self.getTimesFromFilters()
        results = self.REPORT_FUNCS[rep_type](times, _db.DB.root)
        self._showResults(results)

    def getTimesFromFilters(self):
        """Returns a touple of times from the date widgets.
                         The data format is the same as the key in move_list
                """
        return _utils.getTimesFromFilters(self.widget.dMin, self.widget.dMax)

    @_qc.Slot()
    def export(self):
        report_name = self.REPORT_NAMES[self.widget.cb_type.currentIndex()]
        name = b'banta_report_' + report_name + b'-' + str(datetime.datetime.now()).replace(b':', b'_') + b'.csv'
        fname = _qg.QFileDialog.getSaveFileName(self.app.window, self.widget.tr(b'Guardar Reporte'), name, self.widget.tr(b'Archivos CSV (*.csv);;Todos los archivos (*.*)'))
        fname = fname[0]
        if not fname:
            return False
        writer = csv.writer(open(name, b'wb'), delimiter=b';', quotechar=b'"', quoting=csv.QUOTE_MINIMAL)
        row = []
        for c in range(self.widget.v_list.columnCount()):
            hi = self.widget.v_list.horizontalHeaderItem(c)
            row.append(hi.text().encode(b'utf-8'))

        try:
            writer.writerow(row)
        except:
            pass

        for r in range(self.widget.v_list.rowCount()):
            row = []
            for c in range(self.widget.v_list.columnCount()):
                i = self.widget.v_list.item(r, c)
                row.append(i.text().encode(b'utf-8'))

            try:
                writer.writerow(row)
            except:
                pass

    def _showResults(self, results):
        """Shows the result in the view.
                results is a dictionary.
                the key "_headers" is a list of strings for the headers.
                the other keys represents other rows, must be of a type of Result* with a toStringList() method
                """
        v = self.widget.v_list
        headers = results.pop(b'_headers')
        idx_tag = results.pop(b'_idx_tag')
        idx_val = results.pop(b'_idx_val')
        v.setColumnCount(len(headers))
        v.setHorizontalHeaderLabels(headers)
        v.setRowCount(len(results))
        for r, res in enumerate(sorted(results.values(), reverse=True)):
            for c, t in enumerate(res.toStringList()):
                self.widget.v_list.setItem(r, c, _qg.QTableWidgetItem(t))