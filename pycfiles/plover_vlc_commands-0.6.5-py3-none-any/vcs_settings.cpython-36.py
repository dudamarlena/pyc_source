# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/ui/vcs_settings.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 1256 bytes
from PyQt5.QtWidgets import QFileDialog
from plover.gui_qt.tool import Tool
from plover_vcs.ui.vcs_settings_ui import Ui_VcsSettings
from plover_vcs.vcs_config import VcsConfig, CONFIG_MANAGER

class VcsSettings(Tool, Ui_VcsSettings):
    TITLE = 'Vcs Settings'
    ICON = ':/plover_vcs/icon.svg'

    def __init__(self, engine):
        super(VcsSettings, self).__init__(engine)
        self.setupUi(self)
        self._VcsSettings__engine = engine

    def add_dictionary(self):
        self.dictionariesListWidget.addItem('<dictionary>')

    def remove_dictionary(self):
        for item in self.dictionariesListWidget.selectedItems():
            self.dictionariesListWidget.takeItem(self.dictionariesListWidget.row(item))

    def edit_dictionary(self, item):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select Dictionary File', '', 'JSON Files (*.json)')
        if file_name:
            item.setText(file_name)

    def get_config(self) -> VcsConfig:
        return VcsConfig(self.versionControlSystemComboBox.currentText(), [self.dictionariesListWidget.item(i).text() for i in range(self.dictionariesListWidget.count())])

    def accept(self):
        CONFIG_MANAGER.config = self.get_config()
        super().accept()