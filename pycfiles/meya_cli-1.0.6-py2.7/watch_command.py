# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/watch_command.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
from meya_cli.base_command import BaseCommand

class WatchCommand(BaseCommand):
    INVOCATION = 'watch'
    DESCRIPTION = 'Watch a Meya-managed folder, updating on file changes.'
    ARGUMENTS = [
     (
      'files', {'nargs': '*', 'help': 'files to upload (uploads all files if not present)'})]

    def perform(self):
        from meya_cli.fs_events import MeyaFileSystemEventHandler
        from watchdog.observers import Observer
        event_handler = MeyaFileSystemEventHandler(self.config)
        print('Watching ' + self.config.root_dir)
        observer = Observer()
        observer.schedule(event_handler, self.config.root_dir, recursive=True)
        observer.start()
        try:
            while True:
                event_handler.step(1)

        except KeyboardInterrupt:
            observer.stop()

        observer.join()