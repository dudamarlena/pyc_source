# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-qywz0dnj/ltk/ltk/watchhandler.py
# Compiled at: 2019-11-20 16:41:05
# Size of source mod 2**32: 501 bytes
import ltk.logger as logger
from watchdog.events import FileSystemEventHandler

class WatchHandler(FileSystemEventHandler):

    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def process(self, event):
        logger.info(event.event_type)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)