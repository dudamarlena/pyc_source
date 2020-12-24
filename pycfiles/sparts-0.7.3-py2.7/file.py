# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/file.py
# Compiled at: 2015-07-04 18:06:55
"""Tasks related for files and filesystems"""
from .poller import PollerTask
import errno, os
from ..sparts import option

class DirectoryWatcherTask(PollerTask):
    """DirectoryWatcherTask watches for new, deleted, and modified files
    
    The `IGNORE_INITIAL_FILES` attribute can be overridden to Flaase if you
    do not want to receive a bunch of `onFileCreated` callbacks during startup.

    This could be better implemented with the inotify/pyinotify API, but for
    basic rapid prototyping, polling should be sufficient.
    """
    PATH = '.'
    path = option(default=lambda cls: cls.PATH, help='Directory path to watch [%(default)s]')
    IGNORE_INITIAL_FILES = True

    def onFileCreated(self, filename, stat):
        """Override this to do custom processing when new files are created."""
        self.logger.debug('onFileCreated(%s, %s)', filename, stat)

    def onFileDeleted(self, filename, old_stat):
        """Override this to do custom processing when files are deleted."""
        self.logger.debug('onFileDeleted(%s, %s)', filename, old_stat)

    def onFileChanged(self, filename, old_stat, new_stat):
        """Override this to do custom processing when files are modified."""
        self.logger.debug('onFileChanged(%s, %s, %s)', filename, old_stat, new_stat)

    def fetch(self):
        """Overridden to stat a particular filesystem path"""
        root = self.path
        try:
            contents = self.listdir(root)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
            self.logger.warning("Unable to read directory, '%s' (ENOENT)", root)
            contents = []

        d = {}
        for name in contents:
            try:
                d[name] = self.stat(os.path.join(root, name))
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

        return sorted(d.items())

    def onValueChanged(self, old_value, new_value):
        """Overridden to track file statuses."""
        if old_value is None:
            if self.IGNORE_INITIAL_FILES:
                return
            old_value = []
        old_value_dict = dict(old_value)
        new_value_dict = dict(new_value)
        for name, old_stat in old_value:
            if name not in new_value_dict:
                self.onFileDeleted(name, old_stat)
            else:
                new_stat = new_value_dict[name]
                if new_stat != old_stat:
                    self.onFileChanged(name, old_stat, new_stat)

        for name, new_stat in new_value:
            if name not in old_value_dict:
                self.onFileCreated(name, new_stat)

        return

    def listdir(self, path):
        """Wrapper for making unittesting/mocking easier"""
        return os.listdir(path)

    def stat(self, path):
        """Wrapper for making unittesting/mocking easier"""
        return os.stat(path)