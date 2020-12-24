# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/libs/pyblish/validators/modeling/general/proxymesh.py
# Compiled at: 2020-04-17 19:10:58
# Size of source mod 2**32: 3960 bytes
__doc__ = '\nModule that contains Plot Twist proxy mesh validator implementation\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import pyblish.api, tpDcc, artellapipe

class SelectVerticesWithoutVertexColors(pyblish.api.Action):
    label = 'Select Vertices without Vertex Colors'
    on = 'failed'

    def process(self, context, plugin):
        if not tpDcc.is_maya():
            raise AssertionError('Select Vertices without Vertex Color Action is only available in Maya!')
        else:
            vertices_without_vertex_colors = context.data.get('vertices_without_vertex_colors', None)
            assert vertices_without_vertex_colors, 'No vertices without vertex colors to select'
            vertices_to_select = list()
            for shape_node, vertices_ids in vertices_without_vertex_colors.items():
                for vertex_id in vertices_ids:
                    vertices_to_select.append('{}.vtx[{}]'.format(shape_node, vertex_id))

            assert vertices_to_select, 'No vertices to select'
        tpDcc.Dcc.select_object(vertices_to_select)


class ValidatePlotTwistProxyMesh(pyblish.api.ContextPlugin):
    """ValidatePlotTwistProxyMesh"""
    label = 'General - Check Proxy'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    families = ['proxy']
    optional = False
    actions = [SelectVerticesWithoutVertexColors]

    def process(self, context):
        if not tpDcc.is_maya():
            raise AssertionError('Validate Proxy Mesh is only available in Maya!')
        else:
            from tpDcc.dccs.maya.core import node, api
            root_group_name = artellapipe.NamesMgr().solve_name('root_group')
            proxy_group_name = artellapipe.NamesMgr().solve_name('proxy_group')
            geo_group_name = artellapipe.NamesMgr().solve_name('geo_group')
            proxy_geo = artellapipe.NamesMgr().solve_name('proxy_geo')
            proxy_geo_parent = '{}|{}|{}'.format(root_group_name, proxy_group_name, geo_group_name)
            assert proxy_geo and tpDcc.Dcc.object_exists(proxy_geo), 'Proxy geo "{}" does not exist in current scene!'.format(proxy_geo)
            assert proxy_geo_parent and tpDcc.Dcc.object_exists(proxy_geo_parent), 'Proxy geo parent "{}" does not exists in current scene!'.format(proxy_geo_parent)
            proxy_prefix = proxy_geo.split('_')[0]
            proxy_geos = tpDcc.Dcc.list_nodes(('{}_*'.format(proxy_prefix)), node_type='transform') or list()
            assert len(proxy_geos) == 1, 'Invalid number ({}) of proxy geometries found in current scene: {}'.format(len(proxy_geos), proxy_geos)
            proxy_geo = proxy_geos[0]
            proxy_geo_shapes = tpDcc.Dcc.list_shapes(proxy_geo)
            assert proxy_geo_shapes, 'No sahpes found in proxy geo geometry!'
            vertices_without_vertex_colors = dict()
            for proxy_shape in proxy_geo_shapes:
                proxy_shape_node = node.get_mobject(proxy_shape)
                proxy_shape_vtx_it = api.IterateVertices(proxy_shape_node)
                proxy_shape_vertex_colors = proxy_shape_vtx_it.get_vertex_colors(skip_vertices_without_vertex_colors=False)
                for vtx_id, vtx_color in proxy_shape_vertex_colors.items():
                    if vtx_color:
                        pass
                    else:
                        if proxy_shape not in vertices_without_vertex_colors:
                            vertices_without_vertex_colors[proxy_shape] = list()
                        vertices_without_vertex_colors[proxy_shape].append(vtx_id)

            if vertices_without_vertex_colors:
                context.data['vertices_without_vertex_colors'] = vertices_without_vertex_colors
            assert not vertices_without_vertex_colors, 'Some vertices of the proxy shapes have no vertex color applied to them: {}!'.format(vertices_without_vertex_colors)