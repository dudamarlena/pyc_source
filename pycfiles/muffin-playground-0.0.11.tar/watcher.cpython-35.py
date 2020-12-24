# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fhsu/work/muffin-playground/muffin_playground/watcher.py
# Compiled at: 2016-09-15 20:24:40
# Size of source mod 2**32: 817 bytes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:

    def __init__(self, dir, app):
        self.dir = dir
        self.app = app

    def start(self):
        file_event_callback = self.send_reload_message

        class MyHandler(FileSystemEventHandler):

            def dispatch(self, evt):
                if not evt.is_directory:
                    file_event_callback()

        self.observer = Observer()
        self.observer.schedule(MyHandler(), str(self.dir), recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.join()

    def send_reload_message(self):
        self.app.loop.call_soon_threadsafe(self.app._write_debug_sockets, 'reload')