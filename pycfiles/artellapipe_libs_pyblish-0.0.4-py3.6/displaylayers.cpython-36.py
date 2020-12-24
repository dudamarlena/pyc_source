# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/validators/scene/displaylayers.py
# Compiled at: 2020-04-17 19:10:25
# Size of source mod 2**32: 1653 bytes
"""
Module that contains display layers check validator
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import pyblish.api, tpDcc as tp

class RemoveDisplayLayers(pyblish.api.Action):
    label = 'Remove Display Layers'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Remove From Display Layer Action is only available in Maya!')
            return False
        else:
            import tpDcc.dccs.maya as maya
            maya.cmds.undoInfo(openChunk=True)
            try:
                try:
                    display_layers = maya.cmds.ls(type='displayLayer')
                    for display_layer in display_layers:
                        if display_layer == 'defaultLayer':
                            pass
                        else:
                            maya.cmds.delete(display_layer)

                except Exception as exc:
                    self.log.error('Error while removing display layers: {}'.format(exc))

            finally:
                maya.cmds.undoInfo(closeChunk=False)

            return True


class ValidateDisplayLayers(pyblish.api.ContextPlugin):
    __doc__ = '\n    Checks if current scene has display layers\n    '
    label = 'Scene - Display Layers in Scene'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False
    actions = [RemoveDisplayLayers]

    def process(self, context):
        import maya.cmds as cmds
        layers = cmds.ls(type='displayLayer')
        assert len(layers) == 1, 'Display layers found in current scene: "{}"'.format(layers)