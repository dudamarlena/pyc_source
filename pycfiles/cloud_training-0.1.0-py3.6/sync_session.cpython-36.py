# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\cloud_training\commands\sync_session.py
# Compiled at: 2017-10-30 15:28:44
# Size of source mod 2**32: 1431 bytes
import os
from cloud_training import utils
from cloud_training.project_command import ProjectCommand

class SyncSessionCommand(ProjectCommand):

    def run(self):
        local_training_path = os.path.join(self._project_dir, 'training', self._model)
        s3_training_path = '/'.join([self._s3_project_dir, 'training', self._model])
        session_id = self._args.session
        self._print('Syncing the session "%s"...' % session_id)
        self._aws.s3_sync(s3_training_path + '/' + session_id, os.path.join(local_training_path, session_id), [
         'checkpoints/*'], ['checkpoints/checkpoint'])
        local_checkpoints_path = os.path.join(local_training_path, session_id, 'checkpoints')
        s3_checkpoints_path = s3_training_path + '/' + session_id + '/checkpoints'
        last_model_name = utils.get_last_checkpoint_name(os.path.join(local_checkpoints_path, 'checkpoint'))
        if not last_model_name:
            self._print('Checkpoint was not found')
            return True
        else:
            self._print('Getting the checkpoint "%s"...' % last_model_name)
            self._aws.s3_sync(s3_checkpoints_path, local_checkpoints_path, ['*'], [last_model_name + '*'])
            self._print('Done')
            return True