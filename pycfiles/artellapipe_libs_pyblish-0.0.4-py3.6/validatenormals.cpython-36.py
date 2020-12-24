# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/validators/modeling/topology/validatenormals.py
# Compiled at: 2020-04-17 19:10:25
# Size of source mod 2**32: 1862 bytes
"""
Module that contains normal validation implementation
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import pyblish.api, tpDcc as tp

class UnlockNormals(pyblish.api.Action):
    label = 'Unlock Normals'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Unlock Normals Action is only available in Maya!')
            return False
        import tpDcc.dccs.maya as maya
        for instance in context:
            if not instance.data['publish']:
                pass
            else:
                node = instance.data.get('node')
                for mesh in maya.cmds.listRelatives(node, type='mesh', fullPath=True):
                    faces = maya.cmds.polyListComponentConversion(mesh, toVertexFace=True)
                    maya.cmds.polyNormalPerVertex(faces, edit=True, unFreezeNormal=True)


class ValidateNormals(pyblish.api.InstancePlugin):
    __doc__ = '\n    Normals of a model may not be locked\n    '
    label = 'Topology - Normals'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    families = ['geometry']
    optional = False
    actions = [UnlockNormals]

    def process(self, instance):
        import tpDcc.dccs.maya as maya
        node = instance.data.get('node')
        invalid = list()
        for mesh in maya.cmds.listRelatives(node, type='mesh', fullPath=True):
            faces = maya.cmds.polyListComponentConversion(mesh, toVertexFace=True)
            locked = maya.cmds.polyNormalPerVertex(faces, query=True, freezeNormal=True)
            invalid.append(mesh) if any(locked) else None

        assert not invalid, 'Meshes found with locked normals: {}'.format(invalid)