# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/tools/renamer/widgets/namespacewidget.py
# Compiled at: 2020-04-11 22:50:40
# Size of source mod 2**32: 2810 bytes
"""
Widget that manages namespace rename functionality
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
import tpDcc
from tpDcc.libs.qt.core import base

class NamespaceWidget(base.BaseWidget, object):
    renameUpdate = Signal()
    doAddNamespace = Signal(str)
    doRemoveNamespace = Signal(str)

    def __init__(self, parent=None):
        super(NamespaceWidget, self).__init__(parent=parent)
        self._fill_combo()

    def ui(self):
        super(NamespaceWidget, self).ui()
        namespace_layout = QHBoxLayout()
        namespace_layout.setAlignment(Qt.AlignLeft)
        namespace_layout.setContentsMargins(0, 0, 0, 0)
        namespace_layout.setSpacing(5)
        self.main_layout.addLayout(namespace_layout)
        self._namespace_cbx = QCheckBox()
        self._namespace_line = QLineEdit()
        self._namespace_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._namespace_line.setPlaceholderText('Namespace')
        self._namespace_combo = QComboBox()
        self._namespace_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._combo_icons = [tpDcc.ResourcesMgr().icon('add'), tpDcc.ResourcesMgr().icon('trash')]
        self._namespace_btn = QPushButton()
        self._namespace_btn.setIcon(self._combo_icons[0])
        namespace_layout.addWidget(self._namespace_cbx)
        namespace_layout.addWidget(self._namespace_line)
        namespace_layout.addWidget(self._namespace_combo)
        namespace_layout.addWidget(self._namespace_btn)

    def setup_signals(self):
        self._namespace_combo.currentIndexChanged.connect(self._on_combo_index_changed)
        self._namespace_btn.clicked.connect(self._on_namespace)

    def _fill_combo(self):
        """
        Internal callback function that fills namespace combo
        """
        self._namespace_combo.clear()
        self._namespace_combo.addItems(['Add/Replace', 'Remove'])

    def _on_combo_index_changed(self, index):
        """
        Internal callback function that is called when the user selects a new index in namespace combo
        :param index: int
        """
        self._namespace_btn.setIcon(self._combo_icons[index])

    def _on_namespace(self):
        """
        Internal callback function that is called when namespace button is clicked
        """
        namespace_text = self._namespace_line.text()
        if not namespace_text:
            return
        combo_index = self._namespace_combo.currentIndex()
        if combo_index == 0:
            self.doAddNamespace.emit(namespace_text)
        elif combo_index == 1:
            self.doRemoveNamespace.emit(namespace_text)