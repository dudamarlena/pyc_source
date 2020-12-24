# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/validators/scene/cleanscene.py
# Compiled at: 2020-05-13 18:50:22
# Size of source mod 2**32: 5318 bytes
"""
Module that contains clean scene validator implementation
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import pyblish.api, tpDcc as tp

class CleanUnknownNodes(pyblish.api.Action):
    label = 'Clean Unknown Nodes'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Clean Unknown Nodes Action is only available in Maya!')
        from tpDcc.dccs.maya.core import scene
        scene.delete_unknown_nodes()
        return True


class CleanUnusedPlugins(pyblish.api.Action):
    label = 'Clean Plugin Nodes'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Clean Unused Plugins Action is only available in Maya!')
        from tpDcc.dccs.maya.core import scene
        scene.delete_unused_plugins()
        return True


class CleanTurtleNodes(pyblish.api.Action):
    label = 'Clean Turtle Nodes'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Clean Turtle Nodes Action is only available in Maya!')
        from tpDcc.dccs.maya.core import scene
        scene.delete_turtle_nodes()
        return True


class CleanGarbageNodes(pyblish.api.Action):
    label = 'Clean Garbage Nodes'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Clean Garbage Nodes Action is only available in Maya!')
        from tpDcc.dccs.maya.core import scene
        scene.delete_garbage()
        return True


class ValidateCleanUnknownNodes(pyblish.api.ContextPlugin):
    __doc__ = '\n    Checks if current scene has unknown nodes\n    '
    label = 'Scene - Unknown Nodes'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False
    actions = [CleanUnknownNodes]

    def process(self, context):
        import tpDcc.dccs.maya as maya
        unknown = maya.cmds.ls(type='unknown')
        assert not unknown, 'Unknown nodes found in current scene: {}'.format(unknown)


class ValidateCleanUnusedPlugins(pyblish.api.ContextPlugin):
    __doc__ = '\n    Checks if current scene has unused plugins nodes\n    '
    label = 'Scene - Unused Plugins'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False
    actions = [CleanUnusedPlugins]

    def process(self, context):
        import tpDcc.dccs.maya as maya
        list_cmds = dir(maya.cmds)
        if 'unknownPlugin' not in list_cmds:
            return
        else:
            unknown_plugins = maya.cmds.unknownPlugin(query=True, list=True)
            assert not unknown_plugins, 'Unknown Plugins found in current scene: {}'.format(unknown_plugins)


class ValidateCleanTurtleNodes(pyblish.api.ContextPlugin):
    __doc__ = '\n    Checks if current scene has turtle nodes\n    '
    label = 'Scene - Turtle Nodes'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False
    actions = [CleanTurtleNodes]

    def process(self, context):
        import tpDcc.dccs.maya as maya
        turtle_nodes = list()
        plugin_list = maya.cmds.pluginInfo(query=True, pluginsInUse=True)
        for plugin in plugin_list:
            if plugin[0] == 'Turtle':
                turtle_types = [
                 'ilrBakeLayer',
                 'ilrBakeLayerManager',
                 'ilrOptionsNode',
                 'ilrUIOptionsNode']
                turtle_nodes = maya.cmds.ls(type=turtle_types)
                break

        assert not turtle_nodes, 'Turtle Nodes found in current scene: {}'.format(turtle_nodes)


class ValidateCleanGarbageNodes(pyblish.api.ContextPlugin):
    __doc__ = "\n    Checks if current scene has garbage nodes ('hyperLayout', 'hyperView, empty partitions, empty objectSets, etc)\n    "
    label = 'Scene - Clean Garbage'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False
    actions = [CleanGarbageNodes]

    def process(self, context):
        import tpDcc.dccs.maya as maya
        from tpDcc.dccs.maya.core import helpers, node
        garbage_nodes = list()
        if helpers.get_maya_version() > 2014:
            garbage_nodes = maya.cmds.ls(type=['hyperLayout', 'hyperView'])
            if 'hyperGraphLayout' in garbage_nodes:
                garbage_nodes.remove('hyperGraphLayout')
        else:
            check_connection_node_type = [
             'shadingEngine', 'partition', 'objectSet']
            check_connection_nodes = list()
            for check_type in check_connection_node_type:
                nodes_of_type = maya.cmds.ls(type=check_type)
                check_connection_nodes += nodes_of_type

            nodes_to_skip = ['characterPartition', 'hyperGraphLayout']
            for n in check_connection_nodes:
                if not not n:
                    if not maya.cmds.objExists(n):
                        pass
                    else:
                        if n in nodes_to_skip:
                            pass
                        elif node.is_empty(n):
                            garbage_nodes.append(n)

            assert not garbage_nodes, 'Garbage Nodes found in current scene: {}'.format(garbage_nodes)