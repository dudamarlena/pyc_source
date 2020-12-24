# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/validators/modeling/topology/zeroareafaces.py
# Compiled at: 2020-04-17 19:10:25
# Size of source mod 2**32: 3423 bytes
"""
Module that contains zero area faces validation implementation
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import tpDcc as tp, pyblish.api

class SelectZeroAreaFaces(pyblish.api.Action):
    label = 'Select Zero Area Faces'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Select Zero Area Faces Action is only available in Maya!')
            return False
        for instance in context:
            if not not instance.data['publish']:
                if not instance.data['_has_failed']:
                    pass
                else:
                    node = instance.data.get('node', None)
                    assert node and tp.Dcc.object_exists(node), 'No valid node found in current instance: {}'.format(instance)
                    zero_area_faces = instance.data.get('zero_area_faces', None)
                    assert zero_area_faces, 'No zero area faces geometry found in instance: {}'.format(instance)
                    tp.Dcc.select_object(zero_area_faces, replace_selection=False)


class ValidateZeroAreaFaces(pyblish.api.InstancePlugin):
    __doc__ = '\n    Checks if there are faces with zero area\n    '
    label = 'Topology - Zero Area Faces'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    families = ['geometry']
    optional = False
    actions = [SelectZeroAreaFaces]

    def process(self, instance):
        import maya.api.OpenMaya as OpenMaya
        node = instance.data.get('node', None)
        assert tp.Dcc.object_exists(node), 'No valid node found in current instance: {}'.format(instance)
        nodes_to_check = self._nodes_to_check(node)
        if not nodes_to_check:
            raise AssertionError('No Nodes to check found!')
        else:
            meshes_selection_list = OpenMaya.MSelectionList()
            for node in nodes_to_check:
                meshes_selection_list.add(node)

            zero_area_faces_found = list()
            sel_it = OpenMaya.MItSelectionList(meshes_selection_list)
            while not sel_it.isDone():
                face_it = OpenMaya.MItMeshPolygon(sel_it.getDagPath())
                object_name = sel_it.getDagPath().getPath()
                while not face_it.isDone():
                    zero_area = face_it.zeroArea()
                    face_area = face_it.getArea()
                    if zero_area or face_area < 1e-06:
                        face_index = face_it.index()
                        component_name = '{}.f[{}]'.format(object_name, face_index)
                        zero_area_faces_found.append(component_name)
                    face_it.next(None)

                sel_it.next()

            if zero_area_faces_found:
                instance.data['zero_area_faces'] = zero_area_faces_found
            assert not zero_area_faces_found, 'Zero Area faces found in the following components: {}'.format(zero_area_faces_found)

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