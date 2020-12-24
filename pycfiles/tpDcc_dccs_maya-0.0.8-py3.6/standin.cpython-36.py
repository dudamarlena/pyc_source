# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/standin.py
# Compiled at: 2020-04-24 23:10:50
# Size of source mod 2**32: 2264 bytes
"""
Module that contains Arnold Standin related functionality for Maya
"""
from __future__ import print_function, division, absolute_import
import os, tpDcc.dccs.maya as maya

def is_standin_node(node):
    """
    Returns whether or not given node is a valid Standin cache node
    :param node: str, name of the object to query
    :return: bool
    """
    if not maya.cmds.objExists(node):
        return False
    else:
        if maya.cmds.objectType(node) != 'aiStandIn':
            return False
        return True


def import_standin(ass_path, standin_name=None, namespace='', unique_namespace=True):
    """
    Imports standing file
    :param ass_path: str, standin file path
    :param standin_name: str, standin name. If empty, filename will be used
    :param namespace: str, namesapce of the imported standin node
    :param unique_namespace: bool
    :return:
    """
    if not os.path.isfile(ass_path):
        raise Exception('Standin Path "{}" does not exist!'.format(ass_path))
    else:
        if not maya.cmds.pluginInfo('mtoa.mll', query=True, loaded=True):
            try:
                maya.cmds.loadPlugin('mtoa.mll', quiet=True)
            except Exception:
                raise Exception('Error while loading MtoA Maya plugin!')

            if not standin_name:
                cache_base = os.path.basename(ass_path)
                standin_name = os.path.splitext(cache_base)[0]
        else:
            if namespace:
                if maya.cmds.namespace(ex=namespace):
                    if unique_namespace:
                        index = 1
                        while maya.cmds.namespace(ex=('{}{}'.format(namespace, index))):
                            index += 1

                        namespace = '{}{}'.format(namespace, index)
        ass_node = maya.cmds.createNode('aiStandIn', name=('{}Shape'.format(standin_name)))
        ass_parent = maya.cmds.listRelatives(ass_node, p=True, pa=True)
        ass_parent = maya.cmds.rename(ass_parent, standin_name)
        maya.cmds.setAttr(('{}.dso'.format(ass_node)), ass_path, type='string')
        if namespace:
            if not maya.cmds.namespace(ex=namespace):
                maya.cmds.namespace(add=namespace)
            ass_parent = maya.cmds.rename(ass_parent, '{}:{}'.format(namespace, ass_parent))
            ass_node = maya.cmds.listRelatives(ass_parent, s=True, pa=True)[0]
    return ass_node