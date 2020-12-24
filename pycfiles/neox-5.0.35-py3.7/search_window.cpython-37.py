# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/search_window.py
# Compiled at: 2020-02-26 23:29:02
# Size of source mod 2**32: 15556 bytes
import os
from operator import itemgetter
from datetime import datetime, timedelta, date
from decimal import Decimal
from PyQt5.QtCore import Qt, QVariant, QAbstractTableModel, pyqtSignal, QModelIndex, QSize
from PyQt5.QtWidgets import QTableView, QVBoxLayout, QAbstractItemView, QLineEdit, QDialog, QLabel, QScroller, QHBoxLayout, QScrollArea, QItemDelegate
from PyQt5.QtGui import QPixmap, QIcon
from neox.commons.buttons import ActionButton
__all__ = [
 'Item', 'SearchWindow', 'TableModel']
DELTA_LOCALE = -5
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__, '..', '..')))
ICONS = {'camera':os.path.join(DIR, 'share/icon-camera.svg'), 
 'stock':os.path.join(DIR, 'share/icon-stock.svg')}

class Item(QItemDelegate):

    def __init__(self, values, fields):
        super(Item, self).__init__()
        _ = [setattr(self, n, str(v)) for n, v in zip(fields, values)]


class SearchWindow(QDialog):

    def __init__(self, parent, headers, records, methods, filter_column=[], cols_width=[], title=None, fill=False):
        """
            parent: parent window
            headers: is a list of tuples with name field-column, eg.
                [('name1', 'Name 1'), ...]
            records: is a tuple with two values: a key called 'objects' or 'values',
                and a list of instances values or plain values for build data model:
                [('a' 'b', 'c'), ('d', 'e', 'f')...]
            on_selected_method: method to call when triggered the selection
            filter_column: list of column to search values, eg: [0,2]
            title: title of window
            cols_width: list of width of columns, eg. [120, 60, 280]
            fill: Boolean that define if the table must be fill with all data and
            values and these are visibles
        """
        super(SearchWindow, self).__init__(parent)
        self.parent = parent
        self.headers = headers
        self.records = records
        self.fill = fill
        self.methods = methods
        self.on_selected_method = methods.get('on_selected_method')
        self.on_return_method = methods.get('on_return_method')
        self.filter_column = filter_column
        self.cols_width = cols_width
        self.rows = []
        self.current_row = None
        if not title:
            title = self.tr('SEARCH...')
            self.setWindowTitle(title)
        WIDTH = 550
        if cols_width:
            WIDTH = sum(cols_width) + 130
        self.resize(QSize(WIDTH, 400))
        self.create_table()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        if records:
            if records[0] == 'objects':
                self.set_from_objects(records[1])
            else:
                if records[0] == 'values':
                    self.set_from_values(records[1])
                else:
                    if records[0] == 'data':
                        self.set_from_data(records[1])

    def get_id(self):
        if self.current_row:
            return self.current_row['id']

    def clear_rows(self):
        if self.fill:
            self.table_model.items = []
            self.table_model.currentItems = []
            self.table_model.layoutChanged.emit()

    def clear_filter(self):
        self.filter_field.setText('')
        self.filter_field.setFocus()
        if self.fill:
            self.table_model.items = []
        self.table_view.selectRow(-1)
        self.table_model.currentItems = []
        self.table_model.layoutChanged.emit()

    def set_from_data(self, values):
        if self.fill:
            self.clear_filter()
        self.table_model.set_rows(values, typedata='list')

    def set_from_values(self, values):
        if self.fill:
            self.clear_rows()
        self.table_model.set_rows(values)
        self.update_count_field()

    def update_count_field(self):
        values = self.table_model.currentItems
        self.label_count.setText(str(len(values)))

    def activate_counter(self):
        self.label_control = QLabel('0')
        self.label_control.setObjectName('label_count')
        self.label_control.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.filter_layout.addWidget(self.label_control)

    def set_counter_control(self, val):
        self.label_control.setText(str(len(val)))

    def set_from_objects(self, objects):
        self.rows = []
        for object_ in objects:
            row = []
            for field, _ in self.headers:
                val = getattr(object_, field)
                if hasattr(val, 'name'):
                    val = getattr(val, 'name')
                if isinstance(val, Decimal):
                    val = val
                if isinstance(val, int):
                    val = str(val)
                if isinstance(val, datetime):
                    val = val.strftime('%d/%m/%Y')
                row.append(val)

            self.rows.append(row)

        self.table_model.set_rows(self.rows)

    def create_table(self):
        self.table_model = TableModel(self, (self.rows), (self.headers), (self.filter_column),
          fill=(self.fill))
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setMinimumSize(450, 350)
        self.table_view.setColumnHidden(0, True)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setGridStyle(Qt.DotLine)
        for i in range(len(self.cols_width)):
            self.table_view.setColumnWidth(i, self.cols_width[i])

        vh = self.table_view.verticalHeader()
        vh.setVisible(False)
        hh = self.table_view.horizontalHeader()
        hh.setStretchLastSection(True)
        self.table_view.setSortingEnabled(True)

    def create_widgets(self):
        self.filter_label = QLabel(self.tr('FILTER:'))
        self.filter_field = QLineEdit()
        self.label_count = QLabel('0')
        self.label_count.setObjectName('label_count')
        self.label_count.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.pushButtonOk = ActionButton('ok', self.action_selection_changed)
        self.pushButtonCancel = ActionButton('cancel', self.action_close)

    def create_layout(self):
        layout = QVBoxLayout()
        self.filter_layout = QHBoxLayout()
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_field)
        self.filter_layout.addWidget(self.label_count)
        layout.addLayout(self.filter_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidget(self.table_view)
        layout.addWidget(scroll_area)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.pushButtonCancel)
        buttons_layout.addWidget(self.pushButtonOk)
        layout.addLayout(buttons_layout)
        QScroller.grabGesture(scroll_area, QScroller.LeftMouseButtonGesture)
        self.filter_field.setFocus()
        self.setLayout(layout)

    def create_connections(self):
        self.filter_field.textChanged.connect(self.action_text_changed)
        self.filter_field.returnPressed.connect(self.action_filter_return_pressed)
        self.table_view.clicked.connect(self.action_selection_changed)
        self.table_view.activated.connect(self.action_table_activated)

    def action_table_activated(self):
        pass

    def execute(self):
        self.current_row = None
        self.parent.releaseKeyboard()
        self.filter_field.setFocus()
        return self.exec_()

    def show(self):
        self.parent.releaseKeyboard()
        self.clear_filter()
        self.filter_field.setFocus()
        super(SearchWindow, self).show()

    def hide(self):
        self.parent.grabKeyboard()
        self.parent.setFocus()
        super(SearchWindow, self).hide()

    def action_close(self):
        self.close()

    def action_selection_changed(self):
        selected = self.table_view.currentIndex()
        self.current_row = self.table_model.getCurrentRow(selected)
        if selected.row() < 0:
            self.filter_field.setFocus()
        else:
            column = selected.column()
            name_field = self.table_model.header_fields[column]
            if self.methods.get(name_field):
                parent_method = self.methods[name_field]
                parent_method()
                return
            self.hide()
            if self.parent:
                getattr(self.parent, self.on_selected_method)()
            self.filter_field.setText('')

    def action_text_changed(self):
        self.table_model.setFilter(searchText=(self.filter_field.text()))
        self.update_count_field()
        self.table_model.layoutChanged.emit()

    def action_filter_return_pressed(self):
        if hasattr(self.parent, self.on_return_method):
            method = getattr(self.parent, self.on_return_method)
            method()

    def keyPressEvent--- This code section failed: ---

 L. 262         0  LOAD_FAST                'event'
                2  LOAD_METHOD              key
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'key'

 L. 263         8  LOAD_FAST                'self'
               10  LOAD_ATTR                table_view
               12  LOAD_METHOD              currentIndex
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  STORE_FAST               'selected'

 L. 264        18  LOAD_FAST                'key'
               20  LOAD_GLOBAL              Qt
               22  LOAD_ATTR                Key_Down
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    70  'to 70'

 L. 265        28  LOAD_FAST                'self'
               30  LOAD_ATTR                table_view
               32  LOAD_METHOD              hasFocus
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  POP_JUMP_IF_TRUE    190  'to 190'

 L. 266        38  LOAD_FAST                'self'
               40  LOAD_ATTR                table_view
               42  LOAD_METHOD              setFocus
               44  CALL_METHOD_0         0  '0 positional arguments'
               46  POP_TOP          

 L. 267        48  LOAD_FAST                'self'
               50  LOAD_ATTR                table_view
               52  LOAD_METHOD              selectRow
               54  LOAD_FAST                'selected'
               56  LOAD_METHOD              row
               58  CALL_METHOD_0         0  '0 positional arguments'
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          
               68  JUMP_FORWARD        190  'to 190'
             70_0  COME_FROM            26  '26'

 L. 268        70  LOAD_FAST                'key'
               72  LOAD_GLOBAL              Qt
               74  LOAD_ATTR                Key_Up
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   126  'to 126'

 L. 269        80  LOAD_FAST                'selected'
               82  LOAD_METHOD              row
               84  CALL_METHOD_0         0  '0 positional arguments'
               86  LOAD_CONST               0
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   104  'to 104'

 L. 270        92  LOAD_FAST                'self'
               94  LOAD_ATTR                filter_field
               96  LOAD_METHOD              setFocus
               98  CALL_METHOD_0         0  '0 positional arguments'
              100  POP_TOP          
              102  JUMP_ABSOLUTE       190  'to 190'
            104_0  COME_FROM            90  '90'

 L. 272       104  LOAD_FAST                'self'
              106  LOAD_ATTR                table_view
              108  LOAD_METHOD              selectRow
              110  LOAD_FAST                'selected'
              112  LOAD_METHOD              row
              114  CALL_METHOD_0         0  '0 positional arguments'
              116  LOAD_CONST               1
              118  BINARY_SUBTRACT  
              120  CALL_METHOD_1         1  '1 positional argument'
              122  POP_TOP          
              124  JUMP_FORWARD        190  'to 190'
            126_0  COME_FROM            78  '78'

 L. 273       126  LOAD_FAST                'key'
              128  LOAD_GLOBAL              Qt
              130  LOAD_ATTR                Key_Return
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   170  'to 170'

 L. 274       136  LOAD_FAST                'selected'
              138  LOAD_METHOD              row
              140  CALL_METHOD_0         0  '0 positional arguments'
              142  LOAD_CONST               0
              144  COMPARE_OP               <
              146  POP_JUMP_IF_FALSE   160  'to 160'

 L. 275       148  LOAD_FAST                'self'
              150  LOAD_ATTR                filter_field
              152  LOAD_METHOD              setFocus
              154  CALL_METHOD_0         0  '0 positional arguments'
              156  POP_TOP          
              158  JUMP_ABSOLUTE       190  'to 190'
            160_0  COME_FROM           146  '146'

 L. 277       160  LOAD_FAST                'self'
              162  LOAD_METHOD              action_selection_changed
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  POP_TOP          
              168  JUMP_FORWARD        190  'to 190'
            170_0  COME_FROM           134  '134'

 L. 278       170  LOAD_FAST                'key'
              172  LOAD_GLOBAL              Qt
              174  LOAD_ATTR                Key_Escape
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   190  'to 190'

 L. 279       180  LOAD_FAST                'self'
              182  LOAD_METHOD              hide
              184  CALL_METHOD_0         0  '0 positional arguments'
              186  POP_TOP          
              188  JUMP_FORWARD        190  'to 190'
            190_0  COME_FROM           188  '188'
            190_1  COME_FROM           178  '178'
            190_2  COME_FROM           168  '168'
            190_3  COME_FROM           124  '124'
            190_4  COME_FROM            68  '68'
            190_5  COME_FROM            36  '36'

 L. 282       190  LOAD_GLOBAL              super
              192  LOAD_GLOBAL              SearchWindow
              194  LOAD_FAST                'self'
              196  CALL_FUNCTION_2       2  '2 positional arguments'
              198  LOAD_METHOD              keyPressEvent
              200  LOAD_FAST                'event'
              202  CALL_METHOD_1         1  '1 positional argument'
              204  POP_TOP          

Parse error at or near `CALL_METHOD_1' instruction at offset 202


class TableModel(QAbstractTableModel):
    sigItem_selected = pyqtSignal(str)

    def __init__(self, parent, rows, headers, filter_column=[], fill=False, *args):
        """
            rows: a list of dicts with values
            headers: a list of strings
            filter_column: list of index of columns for use as filter
            fill: If is True ever the rows will be visible
        """
        (QAbstractTableModel.__init__)(self, parent, *args)
        self.rows = rows
        self.fill = fill
        self.header_fields = [h[0] for h in headers]
        self.header_name = [h[1] for h in headers]
        self.rows = []
        self.currentItems = []
        self.items = []
        self.searchField = None
        self.mainColumn = 2
        self.filter_column = filter_column
        self.create_icons()
        if rows:
            if fill:
                self.set_rows(rows)

    def create_icons(self):
        pix_camera = QPixmap()
        pix_camera.load(ICONS['camera'])
        icon_camera = QIcon()
        icon_camera.addPixmap(pix_camera)
        pix_stock = QPixmap()
        pix_stock.load(ICONS['stock'])
        icon_stock = QIcon()
        icon_stock.addPixmap(pix_stock)
        self.icons = {'icon_camera':icon_camera, 
         'icon_stock':icon_stock}

    def _get_item(self, values):
        res = {}
        for name in self.header_fields:
            val = values.get(name)
            if isinstance(val, date):
                val = val.strftime('%d-%m-%Y')
            elif isinstance(val, Decimal) or isinstance(val, float):
                val = '{0:,}'.format(val)
            else:
                if isinstance(val, datetime):
                    mod_hours = val + timedelta(hours=DELTA_LOCALE)
                    val = mod_hours.strftime('%d/%m/%Y %I:%M %p')
                else:
                    if 'icon_' in name:
                        val = self.icons[name]
                    else:
                        if isinstance(val, int):
                            val = str(val)
            res[name] = val

        return res

    def set_rows(self, rows):
        self.beginResetModel()
        self.endResetModel()
        self.rows = rows
        for values in rows:
            self.insertRows(self._get_item(values))

        if self.fill is True:
            self.currentItems = self.items

    def set_rows_list(self, rows):
        self.beginResetModel()
        self.endResetModel()
        for values in rows:
            self.insertRows(Item(values, self.header_fields))

        if self.fill is True:
            self.currentItems = self.items

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return len(self.header_fields)

    def getCurrentRow(self, index):
        row = index.row()
        if self.currentItems:
            if row >= 0:
                if len(self.currentItems) > row:
                    return self.currentItems[row]

    def data(self, index, role, col=None):
        if not index.isValid():
            return
            row = index.row()
            if col is None:
                column = index.column()
            else:
                column = col
            item = None
            if self.currentItems:
                if len(self.currentItems) > row:
                    item = self.currentItems[row]
            name_field = self.header_fields[column]
            if role == Qt.DisplayRole and item:
                if column is not None:
                    return item[name_field]
        elif role == Qt.DecorationRole:
            if item and 'icon_' in name_field:
                return item[name_field]
        elif role == Qt.TextAlignmentRole:
            if item:
                if 'icon' in name_field:
                    align = Qt.AlignmentFlag(Qt.AlignHCenter)
                    return align
            if item and name_field == 'quantity':
                align = Qt.AlignmentFlag(Qt.AlignCenter)
                return align
        elif role == Qt.UserRole:
            return item

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.header_name[col])
        return QVariant()

    def insertRows(self, item, row=0, column=1, index=QModelIndex()):
        self.beginInsertRows(index, row, row + 1)
        self.items.append(item)
        self.endInsertRows()

    def sort(self, column, order):
        name_field = self.header_fields[column]
        if 'icon_' in name_field:
            return
        data = [(value[name_field], value) for value in self.items]
        data.sort(key=(itemgetter(0)), reverse=order)
        self.currentItems = [v for k, v in data]
        self.layoutChanged.emit()

    def setFilter(self, searchText=None, mainColumn=None, order=None):
        if not searchText:
            return
        else:
            if mainColumn is not None:
                self.mainColumn = mainColumn
            self.order = order
            self.currentItems = self.items
            if searchText and self.filter_column:
                matchers = [t.lower() for t in searchText.split(' ')]
                self.filteredItems = []
                for item in self.currentItems:
                    values_clear = list([_f for _f in list(item.values()) if _f])
                    exists = all((mt in ''.join(values_clear).lower() for mt in matchers))
                    if exists:
                        self.filteredItems.append(item)

                self.currentItems = self.filteredItems
        self.layoutChanged.emit()

    def clear_filter(self):
        if self.fill:
            self.items = []
        self.currentItems = []
        self.layoutChanged.emit()