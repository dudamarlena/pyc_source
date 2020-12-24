# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/playblastmanager/plugins/stamp.py
# Compiled at: 2020-05-03 22:03:42
# Size of source mod 2**32: 1909 bytes
"""
Module that contains implementation for Playblast Stamp Plugin
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from tpDcc.libs.qt.widgets import layouts, checkbox
from artellapipe.tools.playblastmanager.core import plugin

class StampWidget(plugin.PlayblastPlugin, object):
    id = 'Stamp'
    collapsed = True

    def __init__(self, project, config, parent=None):
        super(StampWidget, self).__init__(project=project, config=config, parent=parent)

    def get_main_layout(self):
        main_layout = layouts.VerticalLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        return main_layout

    def ui(self):
        super(StampWidget, self).ui()
        self.enable_cbx = checkbox.BaseCheckBox('Enable')
        self.main_layout.addWidget(self.enable_cbx)

    def get_inputs(self, as_preset=False):
        """
        Overrides base ArtellaPlayblastPlugin get_inputs function
        Returns a dict with proper input variables as keys of the dictionary
        :return: dict
        """
        return {'enable_stamp': self.enable_cbx.isChecked()}

    def get_outputs(self):
        """
        Overrides base ArtellaPlayblastPlugin get_outputs function
        Returns the outputs variables of the Playblast widget as dict
        :return: dict
        """
        return {'enable_stamp': self.enable_cbx.isChecked()}

    def apply_inputs(self, attrs_dict):
        """
        Overrides base ArtellaPlayblastPlugin apply_inputs function
        Applies the given dict of attributes to the widget
        :param attrs_dict: dict
        """
        enable = attrs_dict.get('enable_stamp', True)
        self.enable_cbx.setChecked(enable)