# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/validators/modeling/general/visibility.py
# Compiled at: 2020-05-13 18:50:22
# Size of source mod 2**32: 3086 bytes
"""
Module that contains geometry visibility validator implementation
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import tpDcc as tp, pyblish.api

class ShowGeometry(pyblish.api.Action):
    label = 'Shows Geometry'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Show Geometry Action is only available in Maya!')
            return False
        else:
            import tpDcc.dccs.maya as maya
            maya.cmds.undoInfo(openChunk=True)
            try:
                try:
                    for instance in context:
                        if not instance.data['publish']:
                            pass
                        else:
                            shapes_to_smooth = instance.data.get('nodes_to_make_visible', None)
                            if not shapes_to_smooth:
                                pass
                            else:
                                for shape in shapes_to_smooth:
                                    tp.Dcc.set_attribute_value(shape, 'visibility', True)

                except Exception as exc:
                    self.log.error('Error while disabling smooth preview from shapes: {}'.format(exc))

            finally:
                maya.cmds.undoInfo(openChunk=False)

            return True


class ValidateGeometryVisibility(pyblish.api.InstancePlugin):
    __doc__ = '\n    Checks if mesh is visible or not\n    '
    label = 'General - Geometry Visibility'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    families = ['geometry']
    optional = False
    actions = [ShowGeometry]

    def process(self, instance):
        node = instance.data.get('node', None)
        if not tp.Dcc.object_exists(node):
            raise AssertionError('No valid node found in current instance: {}'.format(instance))
        else:
            nodes_to_check = self._nodes_to_check(node)
            assert nodes_to_check, 'No Nodes to check found!'
            nodes_to_make_visible = list()
            for node in nodes_to_check:
                is_vis = tp.Dcc.get_attribute_value(node, 'visibility')
                if not is_vis:
                    nodes_to_make_visible.append(node)
                shapes = tp.Dcc.list_shapes(node)
                for shape in shapes:
                    is_vis = tp.Dcc.get_attribute_value(shape, 'visibility')
                    if not is_vis:
                        nodes_to_make_visible.append(shape)

            instance.data['nodes_to_make_visible'] = nodes_to_make_visible
            assert not nodes_to_make_visible, 'Following geometry nodes have shapes with Smooth Preview enabled: {}'.format(nodes_to_make_visible)

    def _nodes_to_check(self, node):
        valid_nodes = list()
        nodes = tp.Dcc.list_children(node=node, all_hierarchy=True, full_path=True, children_type='transform')
        if not nodes:
            nodes = [
             node]
        else:
            nodes.append(node)
        for node in nodes:
            shapes = tp.Dcc.list_shapes(node=node, full_path=True)
            if not shapes:
                pass
            else:
                valid_nodes.append(node)

        return valid_nodes