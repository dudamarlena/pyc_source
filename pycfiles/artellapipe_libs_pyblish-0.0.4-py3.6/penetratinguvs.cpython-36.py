# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/validators/modeling/uvs/penetratinguvs.py
# Compiled at: 2020-04-17 19:10:25
# Size of source mod 2**32: 2015 bytes
"""
Module that contains penetrating uvs validation implementation
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import tpDcc as tp, pyblish.api

class ValidatePenetratingUVs(pyblish.api.InstancePlugin):
    __doc__ = '\n    Checks if a geometry node has its UVs penetrating or not\n    '
    label = 'UVs - Penetrating UVs'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    families = ['geometry']
    must_pass = True

    def process(self, instance):
        import maya.cmds as cmds
        node = instance.data.get('node', None)
        if not tp.Dcc.object_exists(node):
            raise AssertionError('No valid node found in current instance: {}'.format(instance))
        else:
            nodes_to_check = self._nodes_to_check(node)
            assert nodes_to_check, 'No Nodes to check found!'
            penetrating_uvs_found = list()
            for node in nodes_to_check:
                shape = tp.Dcc.list_shapes(node, full_path=True)
                convert_to_faces = cmds.ls(cmds.polyListComponentConversion(shape, tf=True), fl=True)
                overlapping = cmds.polyUVOverlap(convert_to_faces, oc=True)
                if overlapping:
                    for obj in overlapping:
                        penetrating_uvs_found.append(obj)

            assert not penetrating_uvs_found, 'Penetrating UVs found in following geometry nodes: {}'.format(penetrating_uvs_found)

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