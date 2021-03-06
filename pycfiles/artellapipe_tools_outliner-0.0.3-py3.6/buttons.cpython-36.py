# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/outliner/widgets/buttons.py
# Compiled at: 2020-03-13 14:11:09
# Size of source mod 2**32: 1062 bytes
"""
Module that contains item buttons for Outliner
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from artellapipe.tools.outliner.core import buttons
from Qt.QtWidgets import *

class ModelDisplayButtons(buttons.DisplayButtonsWidget, object):

    def __init__(self, parent=None):
        super(ModelDisplayButtons, self).__init__(parent=parent)

    def custom_ui(self):
        self.setMinimumWidth(25)
        self.proxy_hires_cbx = QComboBox()
        self.proxy_hires_cbx.addItem('proxy')
        self.proxy_hires_cbx.addItem('hires')
        self.proxy_hires_cbx.addItem('both')
        self.main_layout.addWidget(self.proxy_hires_cbx)


class ArtellaDisplayButtons(buttons.DisplayButtonsWidget, object):

    def __init__(self, parent=None):
        super(ArtellaDisplayButtons, self).__init__(parent=parent)

    def custom_ui(self):
        self.setMinimumWidth(25)