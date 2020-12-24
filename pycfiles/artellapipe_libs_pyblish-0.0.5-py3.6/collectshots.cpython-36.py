# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/collectors/layout/collectshots.py
# Compiled at: 2020-05-13 18:50:22
# Size of source mod 2**32: 815 bytes
import os, pyblish.api, artellapipe

class CollectShots(pyblish.api.ContextPlugin):
    label = 'Collect Shots'
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
        shots = cmds.ls(type='shot')
        for shot in shots:
            shot_node = artellapipe.ShotsMgr().find_shot(shot)
            if not shot_node:
                continue
            instance = context.create_instance(shot, project=project)
            instance.data['shot'] = shot_node
            instance.data['family'] = 'shots'