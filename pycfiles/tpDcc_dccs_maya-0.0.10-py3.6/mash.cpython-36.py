# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/mash.py
# Compiled at: 2020-05-13 19:28:33
# Size of source mod 2**32: 2834 bytes
"""
Module that contains functions and classes related with MASH nodes
"""
from __future__ import print_function, division, absolute_import
MASH_AVAILABLE = True
try:
    import MASH.api as mapi, MASH.undo as undo, MASHoutliner, mash_repro_utils, mash_repro_aetemplate
except ImportError:
    MASH_AVAILABLE = False

import tpDcc.dccs.maya as maya
from tpDcc.dccs.maya.core import name as naming, gui

def get_mash_nodes():
    """
    Returns a list with all MASH nodes in current Maya scene
    :return: list<str>
    """
    return maya.cmds.ls(type='MASH_Waiter')


def create_mash_network(name='New_Mash_Network', type='repro'):
    name = naming.find_available_name(name=name)
    if type == 'instancer':
        maya.mel.eval('optionVar -iv mOGT 1;')
    else:
        if type == 'repro':
            maya.mel.eval('optionVar -iv mOGT 2;')
    waiter_node = maya.mel.eval('MASHnewNetwork("{0}")'.format(name))[0]
    mash_network = get_mash_network(waiter_node)
    return mash_network


def get_mash_network(node_name):
    if maya.cmds.objExists(node_name):
        return mapi.Network(node_name)


if MASH_AVAILABLE:

    @undo.chunk('Removing MASH Network')
    def remove_mash_network(network):
        print(type(network))
        if type(network) == unicode:
            network = get_mash_network(network)
        if network:
            if maya.cmds.objExists(network.instancer):
                maya.cmds.delete(network.instancer)
            else:
                if maya.cmds.objExists(network.distribute):
                    maya.cmds.delete(network.distribute)
                if maya.cmds.objExists(network.waiter):
                    maya.cmds.delete(network.waiter)


def get_mash_outliner_tree():
    return MASHoutliner.OutlinerTreeView()


if MASH_AVAILABLE:

    @undo.chunk
    def add_mesh_to_repro(repro_node, meshes=None):
        maya.cmds.undoInfo(ock=True)
        if meshes is None:
            meshes = maya.cmds.ls(sl=True)
        for obj in meshes:
            if maya.cmds.objectType(obj) == 'mesh':
                obj = maya.cmds.listRelatives(obj, parent=True)[0]
            if maya.cmds.listRelatives(obj, ad=True, type='mesh'):
                mash_repro_utils.connect.mesh_group(repro_node, obj)

        maya.cmds.undoInfo(cck=True)


def get_repro_object_widget(repro_node):
    if not repro_node:
        return
    maya_window = gui.get_maya_window()
    repro_widgets = maya_window.findChildren(mash_repro_aetemplate.ObjectsWidget) or []
    if len(repro_widgets) > 0:
        return repro_widgets[0]


def set_repro_object_widget_enabled(repro_node, flag):
    repro_widget = get_repro_object_widget(repro_node)
    if not repro_widget:
        return
    repro_widget.parent().parent().setEnabled(flag)