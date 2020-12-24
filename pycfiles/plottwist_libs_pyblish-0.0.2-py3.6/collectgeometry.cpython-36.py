# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/libs/pyblish/collectors/modeling/collectgeometry.py
# Compiled at: 2020-04-17 19:10:58
# Size of source mod 2**32: 996 bytes
import pyblish.api, artellapipe

class CollectPlotTwistGeometry(pyblish.api.ContextPlugin):
    label = 'Collect Geometry'
    order = pyblish.api.CollectorOrder
    hosts = ['maya']

    def process(self, context):
        import maya.cmds as cmds
        project = None
        for name, value in artellapipe.__dict__.items():
            if name == 'project':
                project = value
                break

        assert project, 'Project not found'
        geo_meshes = cmds.ls(type='mesh', long=True)
        geo_transforms = [cmds.listRelatives(mesh, parent=True, fullPath=True)[0] for mesh in geo_meshes]
        for node in geo_transforms:
            if 'proxy_' in node:
                pass
            else:
                node_name = node.split('|')[(-1)].split(':')[(-1)]
                instance = context.create_instance(node_name, project=project)
                instance.data['icon'] = 'cubes'
                instance.data['node'] = node
                instance.data['family'] = 'geometry'