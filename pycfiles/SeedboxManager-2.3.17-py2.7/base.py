# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tasks/base.py
# Compiled at: 2015-06-14 13:30:57
"""Provides the basic definition for a task.

Also handles execution and basic error handling.
"""
import abc, logging, os, traceback
from oslo_config import cfg
import six
from seedbox.common import timeutil
LOG = logging.getLogger(__name__)
cfg.CONF.import_group('tasks', 'seedbox.options')

@six.add_metaclass(abc.ABCMeta)
class BaseTask(object):
    """Provides the base definition of a task."""

    def __init__(self, media_file):
        self.media_file = media_file
        self.gen_files = []

    def __call__(self):
        """Provides ability to execute the task in a consistent manner."""
        try:
            _start = timeutil.utcnow()
            self.execute()
            self.media_file.total_time = timeutil.delta_seconds(_start, timeutil.utcnow())
        except Exception:
            self.media_file.error_msg = traceback.format_exc()

        self.gen_files.append(self.media_file)
        return self.gen_files

    def add_gen_files(self, files):
        """Adds media files included within an archived file.

        Enables parallel processing.

        :param files: a list of media files produced by a plugin to be
                      included on the torrent.
        """
        _cls = type(self.media_file)
        _base = self.media_file.as_dict()
        _base['media_id'] = None
        _base['file_path'] = cfg.CONF.tasks.sync_path
        _base['compressed'] = False
        _base['synced'] = False
        _base['missing'] = False
        _base['skipped'] = False
        _base['error_msg'] = None
        _base['total_time'] = None
        for mf in files:
            _base['filename'] = mf
            _, _base['file_ext'] = os.path.splitext(mf)
            _base['size'] = os.path.getsize(os.path.join(cfg.CONF.tasks.sync_path, mf))
            self.gen_files.append(_cls(**_base))

        LOG.debug('gen_files: %s', self.gen_files)
        return

    @staticmethod
    def is_actionable(media_file):
        """Perform check to determine if action should be taken.

        :param media_file: the file to inspect to determine
                           if action is necessary
        :returns: a flag indicating to act or not to act
        :rtype: boolean
        """
        return True

    @abc.abstractmethod
    def execute(self):
        """Perform action associated with task for the provided media_file."""
        raise NotImplementedError

    def __str__(self):
        return ('{0}: {1}').format(self.__class__.__name__, self.__dict__)

    __repr__ = __str__