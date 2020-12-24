# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\base\csv_imports.py
# Compiled at: 2013-01-09 09:45:22
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import csv, PySide.QtCore as _qc, PySide.QtGui as _qg, banta.packages as _pkg, banta.db as _db

class CSVImports(_pkg.GenericModule):
    REQUIRES = (
     _pkg.GenericModule.P_ADMIN,)
    NAME = b'csvimports'

    def load(self):
        self.app.window.acImportProducts.triggered.connect(self.importProducts)
        self.app.window.acImportClients.triggered.connect(self.importClients)
        self.app.window.acImportProviders.triggered.connect(self.importProviders)

    @_qc.Slot()
    def importProducts(self):
        """Handles importing data from a csv file"""
        msg = self.app.window.tr(b'Elija un archivo .csv cuyas columnas sean:\nCódigo, Nombre, Precio, Stock, Tipo de Iva [0, 1 o 2], Código de Proveedor')
        _qg.QMessageBox.information(self.app.window, b'Banta', msg)
        fname = _qg.QFileDialog.getOpenFileName(self.app.window, self.app.window.tr(b'Abrir archivo'), b'', self.app.window.tr(b'Archivos CSV (*.csv);;Todos los archivos (*.*)'))
        fname = fname[0]
        if not fname:
            return False
        else:
            f = open(fname, b'rb')
            delim = (b';').encode(b'ascii')
            quote = (b'"').encode(b'ascii')
            reader = csv.reader(f, delimiter=delim, quotechar=quote)
            updated = discarded = inserted = 0
            mod_name = _pkg.base.products.Products.NAME
            prod_model = self.app.modules[mod_name].model
            prod_model.beginResetModel()
            try:
                for art in reader:
                    code = art and art.pop(0) or None
                    name = art and art.pop(0) or b''
                    price = art and art.pop(0) or b'0'
                    stock = art and art.pop(0) or b'0'
                    tax_type = art and art.pop(0) or b'0'
                    prov = art and art.pop(0) or b''
                    if name:
                        name = name.decode(b'utf-8', b'replace')
                    else:
                        name = b''
                    if not code:
                        logger.info(b'Invalid code for product (%s)' % name)
                        discarded += 1
                        continue
                    code = code.decode(b'utf-8', b'replace')
                    try:
                        price = float(price)
                    except:
                        price = 0.0

                    try:
                        stock = float(stock)
                    except:
                        stock = 0.0

                    try:
                        tax_type = int(tax_type)
                    except:
                        tax_type = 1

                    if code in _db.DB.products:
                        prod = _db.DB.products[code]
                        updated += 1
                    else:
                        prod = _db.models.Product(code)
                        _db.DB.products[code] = prod
                        inserted += 1
                    prod.name = name
                    prod.price = price
                    prod.stock = stock
                    prod.tax_type = tax_type
                    if prov in _db.DB.providers:
                        prod.provider = _db.DB.providers[prov]

                _db.DB.commit(b'user', b'product import')
                msg = self.app.window.tr(b'%s productos agregados\n%s modificados\n%s descartados por código incorrecto')
                msg = msg % (inserted, updated, discarded)
                logger.info(msg)
                _qg.QMessageBox.information(self.app.window, b'Banta', msg)
            except Exception as e:
                _db.DB.abort()
                logger.exception(e)
                _qg.QMessageBox.critical(self.app.window, b'Banta', self.app.window.tr(b'Ha ocurrido un error:\n%s') % e.message)

            prod_model.endResetModel()
            return

    @_qc.Slot()
    def importClients(self):
        """Handles importing data from a csv file"""
        msg = b'Elija un archivo .csv cuyas columnas sean:\n Código, Nombre, Dirección, Tipo de Iva\n'
        msg += b'\tTipos de iva:'
        for t in enumerate(_db.models.Client.TAX_NAMES):
            msg += b'\n\t%s\t%s' % t

        _qg.QMessageBox.information(self.app.window, b'Banta', msg)
        fname = _qg.QFileDialog.getOpenFileName(self.app.window, self.app.window.tr(b'Abrir archivo'), b'', self.app.window.tr(b'Archivos CSV (*.csv);;Todos los archivos (*.*)'))
        fname = fname[0]
        if not fname:
            return False
        f = open(fname, b'rb')
        delim = (b';').encode(b'ascii')
        quote = (b'"').encode(b'ascii')
        reader = csv.reader(f, delimiter=delim, quotechar=quote)
        updated = discarded = inserted = 0
        mod_name = _pkg.base.clients.Clients.NAME
        model = self.app.modules[mod_name].model
        model.beginResetModel()
        try:
            for cli in reader:
                code = cli and cli.pop(0) or b''
                name = cli and cli.pop(0) or b''
                address = cli and cli.pop(0) or b''
                tax_type = cli and cli.pop(0) or b'0'
                if name:
                    name = name.decode(b'utf-8', b'replace')
                else:
                    name = b''
                if not code:
                    logger.info(b'Invalid code for (%s)' % name)
                    discarded += 1
                    continue
                code = code.decode(b'utf-8', b'replace')
                address = address.decode(b'utf-8', b'replace')
                try:
                    tax_type = int(tax_type)
                except:
                    tax_type = 0

                cli = _db.models.Client(code, name=name, address=address, tax_type=tax_type)
                inserted += 1

            msg = self.app.window.tr(b'%s clientes agregados\n%s modificados\n%s descartados por código incorrecto')
            msg = msg % (inserted, updated, discarded)
            logger.info(msg)
            _qg.QMessageBox.information(self.app.window, b'Banta', msg)
            _db.DB.commit(b'', b'client import')
        except Exception as e:
            _db.DB.abort()
            logger.exception(e)
            _qg.QMessageBox.critical(self.app.window, b'Banta', self.app.tr(b'Ha ocurrido un error:\n%s') % e.message)

        model.endResetModel()

    @_qc.Slot()
    def importProviders(self):
        """Handles importing data from a csv file"""
        msg = b'Elija un archivo .csv cuyas columnas sean:\n Código (CUIT), Nombre, Dirección, Teléfono, Mail\n'
        _qg.QMessageBox.information(self.app.window, b'Banta', msg)
        fname = _qg.QFileDialog.getOpenFileName(self.app.window, self.app.window.tr(b'Abrir archivo'), b'', self.app.window.tr(b'Archivos CSV (*.csv);;Todos los archivos (*.*)'))
        fname = fname[0]
        if not fname:
            return False
        f = open(fname, b'rb')
        delim = (b';').encode(b'ascii')
        quote = (b'"').encode(b'ascii')
        reader = csv.reader(f, delimiter=delim, quotechar=quote)
        updated = discarded = inserted = 0
        mod_name = _pkg.base.providers.Providers.NAME
        model = self.app.modules[mod_name].model
        model.beginResetModel()
        try:
            for prov in reader:
                code = prov and prov.pop(0) or b''
                name = prov and prov.pop(0) or b''
                address = prov and prov.pop(0) or b''
                phone = prov and prov.pop(0) or b''
                mail = prov and prov.pop(0) or b''
                if name:
                    name = name.decode(b'utf-8', b'replace')
                else:
                    name = b''
                if not code:
                    logger.debug(b'Invalid code for (%s)' % name)
                    discarded += 1
                    continue
                code = code.decode(b'utf-8', b'replace')
                address = address.decode(b'utf-8', b'replace')
                phone = phone.decode(b'utf-8', b'replace')
                mail = mail.decode(b'utf-8', b'replace')
                if code in _db.DB.providers:
                    pro = _db.DB.providers[code]
                    updated += 1
                else:
                    pro = _db.models.Provider(code)
                    _db.DB.providers[code] = pro
                    inserted += 1
                pro.name = name
                pro.address = address
                pro.phone = phone
                pro.mail = mail

            msg = self.app.window.tr(b'%s proveedores agregados\n%s modificados\n%s descartados por código incorrecto')
            msg = msg % (inserted, updated, discarded)
            logger.info(msg)
            _qg.QMessageBox.information(self.app.window, b'Banta', msg)
            _db.DB.commit(b'', b'providers import')
        except Exception as e:
            _db.DB.abort()
            logger.exception(e)
            _qg.QMessageBox.critical(self.app.window, b'Banta', self.app.tr(b'Ha ocurrido un error:\n%s') % e.message)

        model.endResetModel()