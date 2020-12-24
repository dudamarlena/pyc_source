# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tasks/filecopy.py
# Compiled at: 2015-06-14 13:30:57
"""CopyFile task plugin for copying a file to specified location."""
import logging, os, shutil
from oslo_config import cfg
from seedbox.tasks import base
LOG = logging.getLogger(__name__)
cfg.CONF.import_group('tasks', 'seedbox.options')

class CopyFile(base.BaseTask):
    """Provides the capability of copying files locally."""

    @staticmethod
    def is_actionable(media_file):
        """Perform check to determine if action should be taken.

        :param media_file: an instance of a MediaFile to check
        :returns: a flag indicating to act or not to act
        :rtype: boolean
        """
        return not media_file.compressed and media_file.file_path != cfg.CONF.tasks.sync_path

    def execute(self):
        """Perform copying action for the provided media_file."""
        LOG.debug('copying file: %s', self.media_file.filename)
        shutil.copy2(os.path.join(self.media_file.file_path, self.media_file.filename), cfg.CONF.tasks.sync_path)
        self.media_file.file_path = cfg.CONF.tasks.sync_path