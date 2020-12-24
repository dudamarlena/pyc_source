# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/tagger/editors/shaderseditor.py
# Compiled at: 2020-03-08 13:23:53
# Size of source mod 2**32: 3746 bytes
"""
Module that contains implementation for shaders editor
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from functools import partial
from Qt.QtWidgets import *
import tpDcc as tp, artellapipe
from artellapipe.tools.tagger.widgets import taggereditor

class ShadersEditor(taggereditor.TaggerEditor, object):
    EDITOR_TYPE = 'Shaders'

    def __init__(self, project, parent=None):
        super(ShadersEditor, self).__init__(project=project, parent=parent)

    def ui(self):
        super(ShadersEditor, self).ui()
        self._update_shaders_btn = QPushButton('Update Shaders')
        self.main_layout.addWidget(self._update_shaders_btn)

    def setup_signals(self):
        self._update_shaders_btn.clicked.connect(partial(self.update_data, None))

    def initialize(self):
        """
        Initializes tagger editor
        """
        pass

    def reset(self):
        """
        Function that resets all editor information
        """
        pass

    def update_tag_buttons_state(self, sel=None):
        """
        Updates the selection tag attribute of the tag data node
        :param name: str, name of the selection tag to add/remove
        """
        tag_data_node = artellapipe.TagsMgr().get_tag_data_node_from_current_selection(sel)
        if tag_data_node is None:
            return
        attr_exists = tp.Dcc.attribute_exists(node=tag_data_node, attribute_name='shaders')
        if attr_exists:
            pass

    def fill_tag_node(self, tag_data_node, *args, **kwargs):
        """
        Fills given tag node with the data managed by this editor
        :param tag_data_node: str
        """
        sel = kwargs.pop('sel', None)
        tag_data_node = artellapipe.TagsMgr().get_tag_data_node_from_current_selection(sel)
        if tag_data_node is None:
            return
        attr_exists = tp.Dcc.attribute_exists(node=tag_data_node, attribute_name='shaders')
        if not attr_exists:
            tp.Dcc.add_string_attribute(node=tag_data_node, attribute_name='shaders')
        asset_groups = tp.Dcc.list_nodes(node_name='*_grp', node_type='transform')
        if not asset_groups or len(asset_groups) <= 0:
            return
        self.dataUpdated.emit()