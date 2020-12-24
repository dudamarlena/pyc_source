# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/core/layer.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 1121 bytes
"""
Module that contains functions and classes related with scene layers
"""
from __future__ import print_function, division, absolute_import
import tpMayaLib as maya

def create_display_layer(name, nodes=None, display_type=2):
    """
    Creates a display layer containing given nodes
    :param name: str, name to give to the new display layer
    :param nodes: nodes that should be in the display layer
    :param display_type: int, type of display layer
    """
    if nodes is None:
        nodes = list()
    layer = maya.cmds.createDisplayLayer(name=name)
    maya.cmds.editDisplayLayerMembers(layer, nodes, noRecurse=True)
    maya.cmds.setAttr('{}.displayType'.format(layer), display_type)


def delete_display_layers():
    """
    Deletes all display layers
    """
    layers = maya.cmds.ls(type='displayLayer')
    for ly in layers:
        maya.cmds.delete(ly)


def get_current_render_layer():
    """
    Returns the current Maya render layer
    :return: str
    """
    return maya.cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)