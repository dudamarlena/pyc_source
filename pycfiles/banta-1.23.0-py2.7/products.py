# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\base\products.py
# Compiled at: 2013-02-15 13:19:52
from __future__ import absolute_import, print_function, unicode_literals
import logging, ZODB.blob
logger = logging.getLogger(__name__)
import datetime, csv, PySide.QtCore as _qc, PySide.QtGui as _qg, banta.packages as _pack, banta.packages.optional.categories as _cats, banta.db as _db, banta.utils

class ProductDelegate(_qg.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        self.initStyleOption(option, index)
        col = index.column()
        editor = None
        if col in (0, 1, 2, 11):
            editor = _qg.QLineEdit(parent)
        elif col in (3, 4, 5):
            editor = _qg.QDoubleSpinBox(parent)
            editor.setRange(-2147483646, +2147483646)
        elif col == 6:
            editor = _qg.QComboBox(parent)
            editor.setModel(_pack.base.providers.MODEL)
            editor.setModelColumn(1)
        elif col == 7:
            editor = _qg.QSpinBox(parent)
            editor.setRange(-2147483646, +2147483646)
        elif col == 8:
            editor = _qg.QComboBox(parent)
            editor.setModel(_pack.optional.categories.MODEL)
        elif col == 9:
            editor = _qg.QComboBox(parent)
            editor.setModel(_pack.optional.type_tax.MODEL)
        elif col == 10:
            editor = _qg.QComboBox(parent)
            editor.addItems(_db.models.Product.IB_NAMES)
        return editor

    @_qc.Slot()
    def setEditorData(self, editor, index):
        col = index.column()
        er = _qc.Qt.EditRole
        d = index.data(er)
        if col in (0, 1, 2, 11):
            editor.setText(d)
        elif col in (3, 4, 5, 7):
            editor.setValue(d)
        elif col in (8, 9, 10):
            if d:
                editor.setCurrentIndex(d)
        elif col == 6:
            if d < 0:
                return
            i = editor.findData(d)
            if i < 0:
                return
            editor.setCurrentIndex(i)
        return

    def setModelData(self, editor, model, index):
        col = index.column()
        er = _qc.Qt.EditRole
        if col in (0, 1, 2, 11):
            model.setData(index, editor.text(), er)
        elif col in (3, 4, 5, 7):
            model.setData(index, editor.value(), er)
        elif col in (8, 9, 10):
            model.setData(index, editor.currentIndex(), er)
        elif col == 6:
            i = editor.currentIndex()
            model.setData(index, editor.itemData(i), er)


class ProductModel(_qc.QAbstractTableModel):
    HEADERS = (
     _qc.QT_TRANSLATE_NOOP(b'products', b'Código'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Código Externo'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Nombre'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Precio'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Precio de Compra'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Stock'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Proveedor'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Unidades por caja'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Rubro'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Tipo'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Ingresos Brutos'),
     _qc.QT_TRANSLATE_NOOP(b'products', b'Descripción'))
    max_rows = 0
    columns = 12

    def __init__(self, parent=None):
        _qc.QAbstractTableModel.__init__(self, parent)
        self.parent_widget = parent
        self.tr = banta.utils.unitr(self.trUtf8)
        self._setMaxRows()

    def _setMaxRows(self):
        """Sets the rowcount in the model
                Is Important to call this function when the quantity of products changes
                (in theory that's well managed using this model for adding/removing rows)
                """
        self.max_rows = len(_db.DB.products)

    def rowCount(self, parent=None):
        return self.max_rows

    def columnCount(self, parent=None):
        return self.columns

    def index(self, row, col, parent=None):
        """Creates an index for someone OUTSIDE the model with improved speed"""
        if row < 0 or col < 0 or row >= self.max_rows:
            return self.createIndex(row, col)
        else:
            pro = _db.DB.products.values()[row]
            return self.createIndex(row, col, pro)

    def data(self, index, role=0):
        """Returns the data for a given index, with a given role.
                This is the (most common) way to get the data from the model.
                index is a QModelIndex created by this object ( self.index(row, col) )
                role which role you need (_qc.Qt.EditRole (for editing) _qc.Qt.DisplayRole (for displaying), etc)
                """
        if not index.isValid():
            return
        else:
            if role not in (_qc.Qt.DisplayRole, _qc.Qt.EditRole, _qc.Qt.UserRole, _qc.Qt.DecorationRole):
                return
            pro = index.internalPointer()
            if role == _qc.Qt.UserRole:
                return pro.code
            col = index.column()
            if role == _qc.Qt.DecorationRole:
                if col == 0:
                    try:
                        if pro.thumb:
                            im = pro.thumb.open(b'r')
                            img = _qg.QImage()
                            img.loadFromData(im.read())
                            return img
                        else:
                            return _qg.QImage(b'./static/thumb.jpg')

                    except Exception as e:
                        logger.exception(unicode(e).encode(b'ascii', b'replace'))
                        return

                else:
                    return
            if role == _qc.Qt.EditRole:
                if col == 9:
                    try:
                        return _db.DB.type_tax.index(pro.tax_type)
                    except:
                        return -1

                else:
                    if col == 10:
                        return pro.ib_type
                    if col == 6:
                        if not pro.provider:
                            return -1
                        else:
                            return pro.provider.code

                    elif col == 8:
                        if pro.category is None:
                            return -1
                        try:
                            return _db.DB.categories.index(pro.category)
                        except:
                            return -1

            if col == 0:
                return pro.code
            if col == 1:
                return pro.external_code
            if col == 2:
                return pro.name
            if col == 3:
                return pro.price
            if col == 4:
                return pro.buy_price
            if col == 5:
                return pro.stock
            if col == 6:
                if pro.provider:
                    return pro.provider.name
                return
            if col == 7:
                return pro.pack_units
            if col == 8:
                if pro.category:
                    return pro.category.name
                return
            if col == 9:
                return str(pro.tax_type)
            if col == 10:
                return pro.IBStr()
            if col == 11:
                return pro.description
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
            pro = index.internalPointer()
            col = index.column()
            if col == 0:
                if pro.code == value:
                    return False
                if value in _db.DB.products.keys():
                    _qg.QMessageBox.warning(self.parent_widget, b'Banta', self.tr(b'Ya existe un producto con ese código.'))
                    return False
                del _db.DB.products[pro.code]
                _db.DB.products[value] = pro
                pro.code = value
            elif col == 1:
                pro.external_code = value
            elif col == 2:
                pro.setName(value)
            elif col == 3:
                pro.price = value
            elif col == 4:
                pro.buy_price = value
            elif col == 5:
                title = self.tr(b'Modificar Stock')
                while True:
                    msg, ok = _qg.QInputDialog.getText(self.parent_widget, title, self.tr(b'Razón de la modificación:'), _qg.QLineEdit.Normal, b'')
                    if not ok:
                        return False
                    if msg:
                        move = _db.models.Move(pro, msg, value - pro.stock)
                        pro.stock = value
                        break

            elif col == 6:
                pro.provider = _db.DB.providers[value]
            elif col == 7:
                pro.pack_units = value
            elif col == 8:
                pro.category = _db.DB.categories[value]
            elif col == 9:
                pro.tax_type = _db.DB.type_tax[value]
            elif col == 10:
                pro.ib_type = value
            elif col == 11:
                pro.description = value
            _db.DB.commit()
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, index=None):
        title = self.tr(b'Nuevo Producto')
        for i in range(rows):
            code, ok = _qg.QInputDialog.getText(self.parent_widget, title, self.tr(b'Ingrese el código'), _qg.QLineEdit.Normal, b'')
            if not ok:
                continue
            if code in _db.DB.products.keys():
                _qg.QMessageBox.warning(self.parent_widget, title, self.tr(b'Ya existe un producto con ese código.'))
                continue
            endpos = len(_db.DB.products.keys(max=code, excludemax=True))
            self.beginInsertRows(_qc.QModelIndex(), endpos, endpos)
            prod = _db.models.Product(code, b'-')
            _db.DB.products[prod.code] = prod
            self._setMaxRows()
            self.endInsertRows()
            position += 1

        _db.DB.commit()
        return True

    def removeRows(self, position, rows, index=None):
        self.beginRemoveRows(_qc.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            key = _db.DB.products.keys()[position]
            del _db.DB.products[key]

        _db.DB.commit()
        self._setMaxRows()
        self.endRemoveRows()
        return True

    def endResetModel(self, *args, **kwargs):
        """When there's a massive change in the model, allow the use of begin/endResetModel
                """
        self._setMaxRows()
        _qc.QAbstractTableModel.endResetModel(self, *args, **kwargs)


MODEL = ProductModel()

class Products(_pack.GenericModule):
    REQUIRES = (
     _pack.GenericModule.P_ADMIN,)
    NAME = b'products'

    def __init__(self, app):
        super(Products, self).__init__(app)
        self.model = MODEL
        self.model.parent_widget = app.window
        self.filter_mode = -1

    def load(self):
        import banta.packages.base.providers
        self.proxy_model = _qg.QSortFilterProxyModel(self.app.window.v_products)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(_qc.Qt.CaseInsensitive)
        self.proxy_model.rowsInserted.connect(self.rowInserted, _qc.Qt.QueuedConnection)
        self.app.window.v_products.setModel(self.proxy_model)
        delegate = ProductDelegate(self.app.window)
        self.app.window.v_products.setItemDelegate(delegate)
        self.app.window.cb_billProds.setModel(self.model)
        prov_mod_name = banta.packages.base.providers.Providers.NAME
        prov_model = self.app.modules[prov_mod_name].model
        self.app.window.cb_FilProvider.setModel(prov_model)
        self.app.window.cb_FilProvider.setModelColumn(1)
        self.app.window.cb_FilProvider.setCurrentIndex(-1)
        self.app.window.bProdNew.clicked.connect(self.new)
        self.app.window.bProdDelete.clicked.connect(self.delete)
        self.app.window.bExport.clicked.connect(self.exportProducts)
        self.app.window.bProdClearFilter.clicked.connect(self.clearFilters)
        self.app.window.eProdCode.textChanged.connect(self.nameChanged)
        self.app.window.cb_FilProvider.currentIndexChanged.connect(self.providerChanged)
        self.app.window.bImage.setDefaultAction(self.app.window.acProdImg)
        self.app.window.acProdImg.triggered.connect(self.setImg)

    @_qc.Slot()
    def setImg(self):
        sel = self.app.window.v_products.selectedIndexes()
        if sel:
            i = sel[0]
            fname = _qg.QFileDialog.getOpenFileName(self.app.window, b'Elegir imágen', b'', b'Archivos PNG (*.png);;Archivos JPG (*.jpg);;Todos los archivos (*.*)')[0]
            code = i.data(_qc.Qt.UserRole)
            pro = _db.DB.products[code]
            pro.thumb = ZODB.blob.Blob()
            im = open(fname, b'rb')
            with pro.thumb.open(b'w') as (f):
                f.write(im.read())
            _db.DB.commit()
            self.proxy_model.dataChanged.emit(i, i)

    @_qc.Slot(str)
    def nameChanged(self, name):
        if self.filter_mode != 0:
            self.proxy_model.setFilterKeyColumn(2)
        self.proxy_model.setFilterWildcard(name)
        self.filter_mode = 0

    @_qc.Slot(int)
    def providerChanged(self, i):
        if i < 0:
            return
        if self.filter_mode != 1:
            self.proxy_model.setFilterKeyColumn(6)
            self.proxy_model.setFilterRole(_qc.Qt.EditRole)
        model = self.app.window.cb_FilProvider.model()
        code = model.data(model.index(i, 0), _qc.Qt.EditRole)
        self.proxy_model.setFilterWildcard(code)
        self.filter_mode = 1

    @_qc.Slot()
    def clearFilters(self):
        self.proxy_model.setFilterKeyColumn(0)
        self.proxy_model.setFilterWildcard(None)
        self.app.window.cb_FilProvider.setCurrentIndex(-1)
        self.app.window.eProdCode.setText(b'')
        self.filter_mode = -1
        return

    @_qc.Slot()
    def new(self):
        self.proxy_model.insertRows(0, 1)

    @_qc.Slot(_qc.QModelIndex, int, int)
    def rowInserted(self, parent, start, end):
        """This slot gets called when a row is inserted (read new) when a row is inserted, we dont actually know where
                 it gets inserted because keys are sorted, and key bounds position """
        self.app.window.v_products.selectRow(start)
        sel = self.app.window.v_products.selectedIndexes()
        if sel:
            i = sel[0]
            self.app.window.v_products.scrollTo(i, _qg.QTableView.EnsureVisible)

    @_qc.Slot()
    def delete(self):
        selected = self.app.window.v_products.selectedIndexes()
        if not selected:
            return
        r = selected[0].row()
        self.proxy_model.removeRows(r, 1)

    @_qc.Slot()
    def exportProducts(self):
        name = b'banta_products-' + str(datetime.datetime.now()).replace(b':', b'_') + b'.csv'
        fname = _qg.QFileDialog.getSaveFileName(self.app.window, self.app.window.tr(b'Guardar Reporte'), name, self.app.window.tr(b'Archivos CSV (*.csv);;Todos los archivos (*.*)'))
        fname = fname[0]
        if not fname:
            return False
        delimit = (b';').encode(b'utf-8')
        quote = (b'"').encode(b'utf-8')
        writer = csv.writer(open(fname, b'wb'), delimiter=delimit, quotechar=quote, quoting=csv.QUOTE_MINIMAL)
        row = []
        for c in range(self.app.window.v_products.model().columnCount()):
            hi = self.app.window.v_products.model().headerData(c, _qc.Qt.Horizontal, _qc.Qt.DisplayRole)
            row.append(unicode(hi).encode(b'utf-8'))

        try:
            writer.writerow(row)
        except:
            pass

        self.model.columnCount()
        for r in range(self.app.window.v_products.model().rowCount()):
            row = []
            for c in range(self.app.window.v_products.model().columnCount()):
                index = self.app.window.v_products.model().index(r, c)
                data = self.app.window.v_products.model().data(index, _qc.Qt.DisplayRole)
                row.append(unicode(data).encode(b'utf-8'))

            try:
                writer.writerow(row)
            except:
                pass