# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/assetsmanager/widgets/shotswidget.py
# Compiled at: 2020-04-15 09:21:10
# Size of source mod 2**32: 5557 bytes
"""
Module that contains widget implementation for sequences manager widget
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import logging.config
from Qt.QtCore import *
from Qt.QtWidgets import *
from tpDcc.libs.qt.core import base
import artellapipe
LOGGER = logging.getLogger()

class ShotsWidget(base.BaseWidget, object):
    shotAdded = Signal(object)

    def __init__(self, project, show_viewer_menu=False, parent=None):
        self._project = project
        self._show_viewer_menu = show_viewer_menu
        if not self._project:
            LOGGER.warning('Invalid project for SequencesWidget!')
        super(ShotsWidget, self).__init__(parent=parent)

    def get_main_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        return main_layout

    def ui(self):
        super(ShotsWidget, self).ui()
        self._shots_viewer = artellapipe.ShotsViewer(project=(self._project),
          show_context_menu=(self._show_viewer_menu),
          parent=self)
        self._shots_viewer.first_empty_cell()
        self.main_layout.addWidget(self._shots_viewer)

    def setup_signals(self):
        self._shots_viewer.shotAdded.connect(self.shotAdded.emit)

    def update_shots(self):
        """
        Updates the list of sequences in the sequences viewer
        """
        self._shots_viewer.update_shots()