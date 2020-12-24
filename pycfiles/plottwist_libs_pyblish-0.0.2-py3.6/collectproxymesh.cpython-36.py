# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/libs/pyblish/collectors/modeling/collectproxymesh.py
# Compiled at: 2020-04-17 19:10:58
# Size of source mod 2**32: 870 bytes
import pyblish.api, artellapipe

class CollectPlotTwistProxyMesh(pyblish.api.ContextPlugin):
    label = 'Collect Proxy Mesh'
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
        proxy_geo = artellapipe.NamesMgr().solve_name('proxy_geo')
        if proxy_geo:
            if cmds.objExists(proxy_geo):
                node_name = proxy_geo.split('|')[(-1)].split(':')[(-1)]
                instance = context.create_instance(node_name, project=project)
                instance.data['icon'] = 'cube'
                instance.data['node'] = proxy_geo
                instance.data['family'] = 'proxy'