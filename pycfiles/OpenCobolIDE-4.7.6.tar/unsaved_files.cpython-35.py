# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/dialogs/unsaved_files.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 2043 bytes
"""
This module contains the unsaved files dialog.
"""
from pyqode.qt.QtWidgets import QDialog
from pyqode.core._forms.dlg_unsaved_files_ui import Ui_Dialog
from pyqode.qt import QtWidgets, QtCore

class DlgUnsavedFiles(QDialog, Ui_Dialog):
    __doc__ = '\n    This dialog shows the list of unsaved file in the CodeEditTabWidget.\n\n    Use can choose to:\n    - cancel: nothing changed, no tab will be closed\n    - save all/save selected: save the selected files or all files\n    - discard all changes: nothing will be saved but all tabs will be\n    closed.\n\n    '

    def __init__(self, parent, files=None):
        if files is None:
            files = []
        QtWidgets.QDialog.__init__(self, parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.bt_save_all = self.buttonBox.button(QtWidgets.QDialogButtonBox.SaveAll)
        self.bt_save_all.clicked.connect(self.accept)
        self.discarded = False
        self.bt_discard = self.buttonBox.button(QtWidgets.QDialogButtonBox.Discard)
        self.bt_discard.clicked.connect(self._set_discarded)
        self.bt_discard.clicked.connect(self.accept)
        for file in files:
            self._add_file(file)

        self.listWidget.itemSelectionChanged.connect(self._on_selection_changed)
        self._on_selection_changed()

    def _add_file(self, path):
        icon = QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(path))
        item = QtWidgets.QListWidgetItem(icon, path)
        self.listWidget.addItem(item)

    def _set_discarded(self):
        self.discarded = True

    def _on_selection_changed(self):
        nb_items = len(self.listWidget.selectedItems())
        if nb_items == 0:
            self.bt_save_all.setText(_('Save'))
            self.bt_save_all.setEnabled(False)
        else:
            self.bt_save_all.setEnabled(True)
            self.bt_save_all.setText(_('Save selected'))
        if nb_items == self.listWidget.count():
            self.bt_save_all.setText(_('Save all'))