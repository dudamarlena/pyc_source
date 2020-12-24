# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tasks/fileunrar.py
# Compiled at: 2015-06-14 13:30:57
"""UnrarFile task plugin

For decompressing archived files to specified location.
"""
import logging, os
from oslo_config import cfg
import rarfile
from seedbox.tasks import base
LOG = logging.getLogger(__name__)
cfg.CONF.import_group('tasks', 'seedbox.options')

class UnrarFile(base.BaseTask):
    """Provides the capability of decompressing archived files."""

    @staticmethod
    def is_actionable(media_file):
        """Perform check to determine if action should be taken.

        :param media_file: an instance of a MediaFile to check
        :returns: a flag indicating to act or not to act
        :rtype: boolean
        """
        return media_file.compressed

    def execute(self):
        """Perform file decompression for the provided media_file."""
        LOG.debug('decompressing file %s', self.media_file.filename)
        with rarfile.RarFile(os.path.join(self.media_file.file_path, self.media_file.filename)) as (compressed_file):
            archived_files = compressed_file.namelist()
            compressed_file.extractall(path=cfg.CONF.tasks.sync_path)
        self.add_gen_files(archived_files)
        self.media_file.synced = True