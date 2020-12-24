# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/validators/scene/shownodes.py
# Compiled at: 2020-04-17 19:10:25
# Size of source mod 2**32: 1453 bytes
"""
Module that contains scene visibility validator implementation
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import pyblish.api, tpDcc as tp

class ShowAllNodes(pyblish.api.Action):
    label = 'Show All Nodes'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Show All Nodes Action is only available in Maya!')
        transforms = tp.Dcc.list_nodes(node_type='transform')
        for node in transforms:
            tp.Dcc.show_node(node)

        return True


class ValidateHidedNodes(pyblish.api.ContextPlugin):
    __doc__ = "\n    Checks if current scene has garbage nodes ('hyperLayout', 'hyperView, empty partitions, empty objectSets, etc)\n    "
    label = 'Scene - Hide Nodes'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False
    actions = [ShowAllNodes]

    def process(self, context):
        hide_nodes = list()
        transforms = tp.Dcc.list_nodes(node_type='transform')
        for node in transforms:
            is_visible = tp.Dcc.get_attribute_value(node, 'visibility')
            if not is_visible:
                hide_nodes.append(node)

        assert not hide_nodes, 'Hided nodes found in current scene: {}'.format(hide_nodes)