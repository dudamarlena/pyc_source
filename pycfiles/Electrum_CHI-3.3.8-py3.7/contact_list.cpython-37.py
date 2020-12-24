# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/gui/qt/contact_list.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 5656 bytes
from enum import IntEnum
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QPersistentModelIndex, QModelIndex
from PyQt5.QtWidgets import QAbstractItemView, QMenu
from electrum.i18n import _
from electrum.bitcoin import is_address
from electrum.util import block_explorer_URL
from electrum.plugin import run_hook
from .util import MyTreeView, import_meta_gui, export_meta_gui, webopen

class ContactList(MyTreeView):

    class Columns(IntEnum):
        NAME = 0
        ADDRESS = 1

    headers = {Columns.NAME: _('Name'), 
     Columns.ADDRESS: _('Address')}
    filter_columns = [
     Columns.NAME, Columns.ADDRESS]

    def __init__(self, parent):
        super().__init__(parent, (self.create_menu), stretch_column=(self.Columns.NAME),
          editable_columns=[
         self.Columns.NAME])
        self.setModel(QStandardItemModel(self))
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSortingEnabled(True)
        self.update()

    def on_edited(self, idx, user_role, text):
        _type, prior_name = self.parent.contacts.pop(user_role)
        self.parent.set_contact(text, user_role)
        self.update()

    def import_contacts(self):
        import_meta_gui(self.parent, _('contacts'), self.parent.contacts.import_file, self.update)

    def export_contacts(self):
        export_meta_gui(self.parent, _('contacts'), self.parent.contacts.export_file)

    def create_menu(self, position):
        menu = QMenu()
        idx = self.indexAt(position)
        column = idx.column() or self.Columns.NAME
        selected_keys = []
        for s_idx in self.selected_in_column(self.Columns.NAME):
            sel_key = self.model().itemFromIndex(s_idx).data(Qt.UserRole)
            selected_keys.append(sel_key)

        if selected_keys:
            idx.isValid() or menu.addAction(_('New contact'), lambda : self.parent.new_contact_dialog())
            menu.addAction(_('Import file'), lambda : self.import_contacts())
            menu.addAction(_('Export file'), lambda : self.export_contacts())
        else:
            column_title = self.model().horizontalHeaderItem(column).text()
            column_data = '\n'.join((self.model().itemFromIndex(s_idx).text() for s_idx in self.selected_in_column(column)))
            menu.addAction(_('Copy {}').format(column_title), lambda : self.parent.app.clipboard().setText(column_data))
            if column in self.editable_columns:
                item = self.model().itemFromIndex(idx)
                if item.isEditable():
                    persistent = QPersistentModelIndex(idx)
                    menu.addAction(_('Edit {}').format(column_title), lambda p=persistent: self.edit(QModelIndex(p)))
            menu.addAction(_('Pay to'), lambda : self.parent.payto_contacts(selected_keys))
            menu.addAction(_('Delete'), lambda : self.parent.delete_contacts(selected_keys))
            URLs = [block_explorer_URL(self.config, 'addr', key) for key in filter(is_address, selected_keys)]
            if URLs:
                menu.addAction(_('View on block explorer'), lambda : [webopen(u) for u in URLs])
            run_hook('create_contact_menu', menu, selected_keys)
            menu.exec_(self.viewport().mapToGlobal(position))

    def update(self):
        current_key = self.current_item_user_role(col=(self.Columns.NAME))
        self.model().clear()
        self.update_headers(self.__class__.headers)
        set_current = None
        for key in sorted(self.parent.contacts.keys()):
            contact_type, name = self.parent.contacts[key]
            items = [QStandardItem(x) for x in (name, key)]
            items[self.Columns.NAME].setEditable(contact_type != 'openalias')
            items[self.Columns.ADDRESS].setEditable(False)
            items[self.Columns.NAME].setData(key, Qt.UserRole)
            row_count = self.model().rowCount()
            self.model().insertRow(row_count, items)
            if key == current_key:
                idx = self.model().index(row_count, self.Columns.NAME)
                set_current = QPersistentModelIndex(idx)

        self.set_current_idx(set_current)
        self.sortByColumn(self.Columns.NAME, Qt.AscendingOrder)
        self.filter()
        run_hook('update_contacts_tab', self)