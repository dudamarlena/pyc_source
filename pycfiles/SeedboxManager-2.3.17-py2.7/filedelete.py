# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tasks/filedelete.py
# Compiled at: 2015-06-14 13:30:57
"""DeleteFile task plugin for deleting a file from specified location."""
import logging, os
from oslo_config import cfg
from seedbox.tasks import base
LOG = logging.getLogger(__name__)
cfg.CONF.import_group('tasks', 'seedbox.options')

class DeleteFile(base.BaseTask):
    """Provides capability of deleting file from a specified location."""

    @staticmethod
    def is_actionable(media_file):
        """Perform check to determine if action should be taken.

        :param media_file: an instance of a MediaFile to check
        :returns: a flag indicating to act or not to act
        :rtype: boolean
        """
        return media_file.file_path == cfg.CONF.tasks.sync_path and media_file.synced and os.path.exists(os.path.join(cfg.CONF.tasks.sync_path, media_file.filename))

    def execute(self):
        """Performs file deletion for the provided media_file."""
        LOG.debug('delete file: %s', self.media_file.filename)
        os.remove(os.path.join(cfg.CONF.tasks.sync_path, self.media_file.filename))