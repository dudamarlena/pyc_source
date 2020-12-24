# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/dialogs.py
# Compiled at: 2019-10-27 11:31:28
# Size of source mod 2**32: 12048 bytes
import os
from collections import OrderedDict
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTreeView, QLineEdit, QTableView, QCompleter
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex
from neox.commons.qt_models import get_simple_model
from neox.commons.forms import GridForm
from neox.commons.buttons import ActionButton
__all__ = [
 'QuickDialog', 'SearchDialog', 'HelpDialog', 'FactoryIcons']
current_dir = os.path.dirname(__file__)
_SIZE = (500, 200)

class QuickDialog(QDialog):

    def __init__(self, parent, kind, string=None, data=None, widgets=None, icon=None, size=None, readonly=False):
        super(QuickDialog, self).__init__(parent)
        if not size:
            size = _SIZE
        self.factory = None
        self.readonly = readonly
        self.parent = parent
        self.parent_model = None
        titles = {'warning':self.tr('Warning...'), 
         'info':self.tr('Information...'), 
         'action':self.tr('Action...'), 
         'help':self.tr('Help...'), 
         'error':self.tr('Error...'), 
         'question':self.tr('Question...'), 
         'selection':self.tr('Selection...'), 
         None:self.tr('Dialog...')}
        self.setWindowTitle(titles[kind])
        self.setModal(True)
        self.setParent(parent)
        self.factory = FactoryIcons()
        self.default_widget_focus = None
        self.kind = kind
        self.widgets = widgets
        self.data = data
        string_widget = None
        data_widget = None
        _buttons = None
        row_stretch = 1
        main_vbox = QVBoxLayout()
        self.sub_hbox = QHBoxLayout()
        if string:
            string_widget = QLabel(string)
        if kind == 'help':
            data_widget = widgets[0]
        else:
            if kind == 'action':
                if widgets:
                    data_widget = widgets[0]
                else:
                    data_widget = GridForm(parent, OrderedDict(data))
            else:
                if kind == 'selection':
                    self.name = data['name']
                    data_widget = self.set_selection(parent, data)
                else:
                    if widgets:
                        data_widget = GridForm(parent, OrderedDict(widgets))
                    else:
                        if string_widget:
                            main_vbox.addWidget(string_widget, 0)
                        if data_widget:
                            if isinstance(data_widget, QWidget):
                                row_stretch += 1
                                size = (size[0], size[1] + 200)
                                self.sub_hbox.addWidget(data_widget, 0)
                            else:
                                self.sub_hbox.addLayout(data_widget, 0)
                    self.ok_button = ActionButton('ok', self.dialog_accepted)
                    self.ok_button.setFocus()
                    self.ok_button.setDefault(True)
                    self.cancel_button = ActionButton('cancel', self.dialog_rejected)
                    _buttons = []
        if kind in ('info', 'help', 'warning', 'question', 'error'):
            if kind in ('warning', 'question'):
                _buttons.append(self.cancel_button)
            _buttons.append(self.ok_button)
        else:
            if kind in ('action', 'selection'):
                _buttons.extend([self.cancel_button, self.ok_button])
            self.buttonbox = QHBoxLayout()
            for b in _buttons:
                self.buttonbox.addWidget(b, 1)

            main_vbox.addLayout(self.sub_hbox, 0)
            main_vbox.addLayout(self.buttonbox, 1)
            main_vbox.insertStretch(row_stretch, 0)
            self.setLayout(main_vbox)
            (self.setMinimumSize)(*size)
            if kind in ('info', 'error'):
                self.show()

    def exec_(self, args=None):
        res = None
        self.parent.releaseKeyboard()
        res = super(QuickDialog, self).exec()
        if self.kind == 'action':
            pass
        return res

    def show(self):
        super(QuickDialog, self).show()
        self.parent.releaseKeyboard()
        self.ok_button.setFocus()
        if self.default_widget_focus:
            self.default_widget_focus.setFocus()
            if hasattr(self.default_widget_focus, 'setText'):
                self.default_widget_focus.setText('')
        else:
            self.setFocus()

    def hide(self):
        super(QuickDialog, self).hide()
        self.parent.setFocus()

    def set_info(self, info):
        if hasattr(self, 'label_info'):
            self.label_info.setText(info)

    def set_widgets(self, widgets):
        if widgets:
            self.default_widget_focus = widgets[0]

    def closeEvent(self, event):
        super(QuickDialog, self).closeEvent(event)

    def dialog_rejected(self):
        self.parent.setFocus()
        self.setResult(0)
        self.hide()

    def dialog_accepted(self):
        if self.kind in ('action', 'selection', 'warning', 'question'):
            self.setResult(1)
            self.done(1)
        self.hide()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.dialog_rejected()
        else:
            super(QuickDialog, self).keyPressEvent(event)

    def set_selection(self, obj, data):
        self.set_simple_model()
        setattr(obj, data['name'] + '_model', self.data_model)
        self.parent_model = data.get('parent_model')
        self.treeview = QTreeView()
        self.treeview.setRootIsDecorated(False)
        self.treeview.setColumnHidden(0, True)
        self.treeview.setItemsExpandable(False)
        self.treeview.setAlternatingRowColors(True)
        self.treeview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.treeview.setModel(self.data_model)
        self.treeview.clicked.connect(self.field_selection_changed)
        self.treeview.activated.connect(self.field_selection_changed)
        self.update_values(self.data['values'])
        item = self.data_model.item(0, 0)
        idx = self.data_model.indexFromItem(item)
        self.treeview.setCurrentIndex(idx)
        return self.treeview

    def update_values(self, values):
        self.data_model.removeRows(0, self.data_model.rowCount())
        self._insert_items(self.data_model, values)
        self.treeview.resizeColumnToContents(0)

    def set_simple_model(self):
        self.data_model = QStandardItemModel(0, len(self.data['heads']), self)
        _horizontal = Qt.Horizontal
        for i, h in enumerate(self.data['heads'], 0):
            self.data_model.setHeaderData(i, _horizontal, h)

    def _insert_items(self, model, values):
        for value in values:
            row = []
            for v in value:
                itemx = QStandardItem(v)
                itemx.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                row.append(itemx)

            self.data_model.insertRow(0, row)

        self.data_model.sort(0, Qt.AscendingOrder)

    @pyqtSlot(QModelIndex)
    def field_selection_changed(self, qm_index):
        if not self.readonly:
            item_id = self.data_model.item(qm_index.row(), 0).text()
            item_name = self.data_model.item(qm_index.row(), 1).text()
            if self.parent_model is not None:
                self.parent_model[self.name] = item_id
            elif hasattr(self.parent, 'field_' + self.name):
                field = getattr(self.parent, 'field_' + self.name)
                if hasattr(field, 'setText'):
                    field.setText(item_name)
            else:
                setattr(self.parent, 'field_' + self.name + '_name', item_name)
            setattr(self.parent, 'field_' + self.name + '_id', int(item_id))
            action = getattr(self.parent, 'action_' + self.name + '_selection_changed')
            action()
        self.dialog_accepted()


class SearchDialog(QDialog):

    def __init__(self, parent, headers, values, on_activated, hide_headers=False, completion_column=None, title=None):
        super(SearchDialog, self).__init__(parent)
        self.parent = parent
        self.headers = headers
        self.values = values
        if not title:
            title = self.tr('Search Products...')
        self.setWindowTitle(title)
        self._product_line = QLineEdit()
        self.table_view = QTableView()
        button_cancel = ActionButton('cancel', self.on_reject)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(button_cancel)
        vbox.addWidget(self._product_line)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.completer = QCompleter()
        self.treeview_search_product = QTreeView()
        if hide_headers:
            col_headers = self.treeview_search_product.header()
            col_headers.hide()
        self.completer.setPopup(self.treeview_search_product)
        self._product_line.setCompleter(self.completer)
        self.set_model()
        self.completer.activated.connect(self.on_accept)
        self.completer.setFilterMode(Qt.MatchStartsWith)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionColumn(2)
        self.completer.activated.connect(on_activated)

    def set_model(self):
        headers_name = [h[1] for h in self.headers]
        self.model = get_simple_model(self.parent, self.values, headers_name)
        self.completer.setModel(self.model)

    def get_selected_index(self):
        model_index = self._get_model_index()
        idx = self.model.index(model_index.row(), 0)
        return idx.data()

    def get_selected_data(self):
        model_index = self._get_model_index()
        data = {}
        i = 0
        for h, _ in self.headers:
            data[h] = self.model.index(model_index.row(), i).data()
            i += 1

        return data

    def _get_model_index(self):
        item_view = self.completer.popup()
        index = item_view.currentIndex()
        proxy_model = self.completer.completionModel()
        model_index = proxy_model.mapToSource(index)
        return model_index

    def on_accept(self):
        self.accept()

    def on_reject(self):
        self.reject()


class HelpDialog(QuickDialog):

    def __init__(self, parent):
        self.treeview = QTreeView()
        self.treeview.setRootIsDecorated(False)
        self.treeview.setAlternatingRowColors(True)
        self.treeview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.treeview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        super(HelpDialog, self).__init__(parent, 'help', widgets=[self.treeview], size=(400,
                                                                                        500))
        self.set_info(self.tr('Keys Shortcuts...'))
        self.hide()

    def set_shortcuts(self, shortcuts):
        model = self._help_model(shortcuts)
        self.treeview.setModel(model)
        header = self.treeview.header()
        header.resizeSection(0, 250)

    def _help_model(self, shortcuts):
        model = QStandardItemModel(0, 2, self)
        model.setHeaderData(0, Qt.Horizontal, self.tr('Action'))
        model.setHeaderData(1, Qt.Horizontal, self.tr('Shortcut'))
        for short in shortcuts:
            model.insertRow(0)
            model.setData(model.index(0, 0), short[0])
            model.setData(model.index(0, 1), short[1])

        return model


class FactoryIcons(object):

    def __init__(self):
        name_icons = [
         'print', 'warning', 'info', 'error', 'question']
        self.icons = {}
        for name in name_icons:
            path_icon = os.path.join(current_dir, '..', 'share', 'icon-' + name + '.png')
            if not os.path.exists(path_icon):
                continue
            _qpixmap_icon = QPixmap()
            _qpixmap_icon.load(path_icon)
            _icon_label = QLabel()
            _icon_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
            _icon_label.setPixmap(_qpixmap_icon.scaledToHeight(48))
            self.icons[name] = _icon_label