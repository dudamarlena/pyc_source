# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/vertexcolor.py
# Compiled at: 2020-05-13 19:28:33
# Size of source mod 2**32: 1073 bytes
"""
Module that contains functions and classes related with vertex colors and color sets
"""
from __future__ import print_function, division, absolute_import
from tpDcc.dccs.maya.core import api, node

def get_mesh_vertex_colors(mesh):
    """
    Returns vertex colors applied to given mesh
    :param mesh:, str mesh shape node we want to check for vertex colors
    :return: bool
    """
    mesh_node = node.get_mobject(mesh)
    mesh_vertex_it = api.IterateVertices(mesh_node)
    return mesh_vertex_it.has_vertex_colors()


def check_all_mesh_vertices_has_vertex_colors(mesh):
    """
    Returns whether or not all vertices of the given mesh have vertex colors applied
    :param mesh: str, str mesh shape node we want to check for vertex colors
    :return: bool
    """
    mesh_node = node.get_mobject(mesh)
    mesh_vertex_it = api.IterateVertices(mesh_node)
    mesh_vertex_colors = mesh_vertex_it.get_vertex_colors(skip_vertices_without_vertex_colors=False)
    return None in mesh_vertex_colors.values()