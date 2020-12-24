# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/humberto/src/kytos/kytos-asyncio/kytos/core/napps/napp_dir_listener.py
# Compiled at: 2019-06-06 13:59:39
# Size of source mod 2**32: 2648 bytes
"""Module to monitor installed napps."""
import logging, re
from pathlib import Path
from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer
LOG = logging.getLogger(__name__)

class NAppDirListener(RegexMatchingEventHandler):
    __doc__ = 'Class to handle directory changes.'
    regexes = [
     re.compile('.*\\/kytos\\/napps\\/[a-zA-Z][^/]+\\/[a-zA-Z].*')]
    ignore_regexes = [re.compile('.*\\.installed')]
    _controller = None

    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self.napps_path = self._controller.options.napps
        mode = 511 if self.napps_path.startswith('/var') else 493
        Path(self.napps_path).mkdir(mode=mode, parents=True, exist_ok=True)
        self.observer = Observer()

    def start(self):
        """Start handling directory changes."""
        self.observer.schedule(self, self.napps_path, True)
        self.observer.start()
        LOG.info('NAppDirListener Started...')

    def stop(self):
        """Stop handling directory changes."""
        self.observer.stop()
        LOG.info('NAppDirListener Stopped...')

    def _get_napp(self, absolute_path):
        """Get a username and napp_name from absolute path.

        Args:
            absolute_path(str): String with absolute path.

        Returns:
            tuple: Tuple with username and napp_name.

        """
        relative_path = absolute_path.replace(self.napps_path, '')
        return tuple(relative_path.split('/')[1:3])

    def on_created(self, event):
        """Load a napp from created directory.

        Args:
            event(watchdog.events.DirCreatedEvent): Event received from an
                observer.
        """
        napp = self._get_napp(event.src_path)
        (LOG.debug)(*('The NApp "%s/%s" was enabled.', ), *napp)
        (self._controller.load_napp)(*napp)

    def on_deleted(self, event):
        """Unload a napp from deleted directory.

        Args:
            event(watchdog.events.DirDeletedEvent): Event received from an
                observer.
        """
        napp = self._get_napp(event.src_path)
        (LOG.debug)(*('The NApp "%s/%s" was disabled.', ), *napp)
        (self._controller.unload_napp)(*napp)