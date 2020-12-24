# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpRenamer/widgets/manualrenamewidget.py
# Compiled at: 2019-12-22 00:17:48
# Size of source mod 2**32: 1755 bytes
"""
Widget that contains manual rename widgets for tpRenamer
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from tpQtLib.core import base
from tpRenamer.widgets import renamerwidget, replacerwidget

class ManualRenameWidget(base.BaseWidget, object):
    renameUpdate = Signal()
    replaceUpdate = Signal()

    def __init__(self, parent=None):
        super(ManualRenameWidget, self).__init__(parent=parent)

    def ui(self):
        super(ManualRenameWidget, self).ui()
        self._renamer_widget = renamerwidget.RenamerWidget()
        self._replacer_widget = replacerwidget.ReplacerWidget()
        self.main_layout.addWidget(self._renamer_widget)
        self.main_layout.addWidget(self._replacer_widget)

    def setup_signals(self):
        self._renamer_widget.renameUpdate.connect(self.renameUpdate.emit)
        self._replacer_widget.replaceUpdate.connect(self.replaceUpdate.emit)

    def get_rename_settings(self):
        """
        Function that returns current rename settings
        :return: str, str, str, int, bool, bool, str, bool
        """
        return self._renamer_widget.get_rename_settings()

    def get_replace_settings(self):
        """
        Function that returns current replace settings
        :return: str, str, str, int, bool, bool, str, bool
        """
        return self._replacer_widget.get_replace_settings()