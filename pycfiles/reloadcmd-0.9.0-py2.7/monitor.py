# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/src/monitor.py
# Compiled at: 2016-01-15 21:29:17
import logging
from watchdog.events import FileSystemEventHandler
__all__ = 'Monitor'

class Monitor(FileSystemEventHandler):

    def __init__(self, command, file_ext):
        self.__file_ext = file_ext
        self.executor = Executor(command)
        self.executor.restart()

    def __check_file_type(self, event):
        if not event.is_directory:
            _, ext = os.path.splitext(event.src_path)
            if ext in self.__file_ext:
                return True
        return False

    def on_moved(self, event):
        super(EventHandler, self).on_moved(event)
        if event.is_directory or self.__check_file_type(event):
            what = 'directory' if event.is_directory else 'file'
            logging.debug('Moved %s: from %s to %s', what, event.src_path, event.dest_path)
            self.executor.restart()

    def on_created(self, event):
        super(EventHandler, self).on_created(event)
        if self.__check_file_type(event):
            what = 'directory' if event.is_directory else 'file'
            logging.debug('Created %s: %s', what, event.src_path)
            self.executor.restart()

    def on_deleted(self, event):
        super(EventHandler, self).on_deleted(event)
        if event.is_directory or self.__check_file_type(event):
            what = 'directory' if event.is_directory else 'file'
            logging.debug('Deleted %s: %s', what, event.src_path)
            self.executor.restart()

    def on_modified(self, event):
        super(EventHandler, self).on_modified(event)
        if self.__check_file_type(event):
            what = 'directory' if event.is_directory else 'file'
            logging.debug('Modified %s: %s', what, event.src_path)
            self.executor.restart()