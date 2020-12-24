# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/watchers/fs.py
# Compiled at: 2017-09-11 09:22:47
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ._base import _BaseWatcher
from ..event import Event

class Handler(FileSystemEventHandler):

    def __init__(self, watcher):
        FileSystemEventHandler.__init__(self)
        self._watcher = watcher

    def on_any_event(self, event):
        self._watcher.emit(event)


class FileSystemWatcher(_BaseWatcher, Observer):
    """Observe a location in the file system for changes

    Example:
        .. code-block:: yaml

            watch:
                kind: .fs.FileSystemWatcher
                path: /path/to/observe
                recursive: True

    Args:
        path (str): Path to watch
        recursive (bool, optional): Watch sub directories also, default: False
    """

    def __init__(self, path, recursive=False):
        _BaseWatcher.__init__(self)
        Observer.__init__(self)
        self._path = path
        self._recursive = recursive

    def emit(self, event):
        self._emit(Event(event.event_type, {'is_directory': event.is_directory, 
           'src_path': event.src_path}))

    def start(self):
        self.schedule(Handler(self), self._path, self._recursive)
        super(Observer, self).start()

    def run(self):
        self._log.info('Starting watcher')
        super(Observer, self).run()
        self._log.info('Exiting watcher')

    def stop(self):
        self._log.info('Stopping watcher')
        super(Observer, self).stop()