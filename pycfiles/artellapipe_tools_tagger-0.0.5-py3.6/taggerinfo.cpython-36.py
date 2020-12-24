# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/tagger/widgets/taggerinfo.py
# Compiled at: 2020-05-04 02:49:13
# Size of source mod 2**32: 2443 bytes
"""
Tool used to manage metadata for Artella Assets
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from Qt.QtCore import *
from Qt.QtWidgets import *
import tpDcc
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import dividers
import artellapipe

class TaggerInfoWidget(base.BaseWidget, object):
    createTagNode = Signal()

    def __init__(self, parent=None):
        super(TaggerInfoWidget, self).__init__(parent=parent)

    def ui(self):
        super(TaggerInfoWidget, self).ui()
        frame = QFrame()
        frame.setFrameShadow(QFrame.Sunken)
        frame.setFrameShape(QFrame.StyledPanel)
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.setSpacing(5)
        frame.setLayout(frame_layout)
        self._curr_info_lbl = QLabel('')
        self._curr_info_lbl.setAlignment(Qt.AlignCenter)
        self._new_tagger_node_btn = QPushButton('Create Tag Data node for "{0}"?'.format(artellapipe.TagsMgr().get_current_selection()))
        self._new_tagger_node_btn.setIcon(tpDcc.ResourcesMgr().icon('tag_add'))
        self.main_layout.addWidget(frame)
        frame_layout.addWidget(self._curr_info_lbl)
        frame_layout.addLayout(dividers.DividerLayout())
        frame_layout.addWidget(self._new_tagger_node_btn)

    def setup_signals(self):
        self._new_tagger_node_btn.clicked.connect(self.createTagNode.emit)

    def update_info(self):
        """
        Updates the current widget
        """
        current_selection = artellapipe.TagsMgr().get_current_selection()
        if not artellapipe.TagsMgr().current_selection_has_metadata_node():
            self._curr_info_lbl.setText('Selected object "{0}" has not valid metadata info!'.format(current_selection))
            self._new_tagger_node_btn.setText('Create Tag Data node for "{0}"?'.format(current_selection))
            return
        if not artellapipe.TagsMgr().check_if_current_selected_metadata_node_has_valid_info():
            self._curr_info_lbl.setText('Object "{0}" has not valid Tag Data information!'.format(current_selection))
            return
        self._curr_info_lbl.setText('Object "{0}" valid Tag Data information!'.format(current_selection))