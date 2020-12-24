# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/extractors/layout/shot.py
# Compiled at: 2020-05-13 18:50:22
# Size of source mod 2**32: 3102 bytes
"""
Module that contains layout shot extractor implementation for ArtellaPipe
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os
from distutils import util
import pyblish.api, tpDcc as tp
from tpDcc.libs.python import timedate, osplatform
import artellapipe

class ExportShot(pyblish.api.InstancePlugin):
    label = 'Export Shot'
    order = pyblish.api.ExtractorOrder
    hosts = ['maya']
    families = ['shots']

    def process(self, instance):
        if not instance.data.get('publish', False):
            return False
        else:
            project = instance.data.get('project', None)
            assert project, 'No valid project defined in current instance: {}'.format(instance)
            shots_config = tp.ConfigsMgr().get_config(config_name='artellapipe-shots')
            assert shots_config, 'No valid shots configuration file found in current instance: {}'.format(instance)
            shot_node = instance.data.get('shot', None)
            assert shot_node, 'No valid shot node found in current instance: {}'.format(instance)
            sequence_name = shot_node.get_sequence()
            assert sequence_name, 'No valid sequence name found linked to current instance: {}'.format(instance)
            sequence = artellapipe.SequencesMgr().find_sequence(sequence_name)
            assert sequence, 'No valid sequence found linked to current instance: {}'.format(instance)
            sequence_file_type = sequence.get_file_type('master')
            assert sequence, 'File type "master" not found in current project'
            sequence_file_type.open_file()
            shot_name = shot_node.get_name()
            assert tp.Dcc.object_exists(shot_name), 'No valid shot found in current instance: {}'.format(instance)
            all_shots = artellapipe.ShotsMgr().find_all_shots()
            assert all_shots, 'No shots defined in current project!'
            start_frame = shots_config.get('start_frame', default=101)
            found = False
            for shot in all_shots:
                if shot.get_name() == shot_name:
                    found = True
                    break

            assert found, 'Shot with name: "{}" not found in current sequence!'.format(shot_name)
            new_version = bool(util.strtobool(os.environ.get('{}_SEQUENCES_PUBLISHER_NEW_VERSION'.format(project.get_clean_name().upper()), 'False')))
            base_comment = '{} | {} | Sequences Publisher > Shot "{}" Export'.format(timedate.get_current_time(), osplatform.get_user(True), shot_name)
            comment = instance.data.get('comment', None)
            if comment:
                base_comment = '{} | {}'.format(base_comment, comment)
            valid_export = artellapipe.ShotsMgr().export_shot(shot_name,
              start_frame=start_frame, new_version=new_version, comment=base_comment)
            assert valid_export, 'Shot with name "{}" was not exported successfully!'.format(shot_name)
            return True