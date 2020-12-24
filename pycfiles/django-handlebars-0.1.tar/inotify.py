# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sergii/eclipse-workspaces/django_handlebars/django_handlebars/management/observer/inotify.py
# Compiled at: 2012-03-11 19:55:53
import pyinotify
from base import BaseObserver
__all__ = [
 'Observer']

class Handler(pyinotify.ProcessEvent):

    def my_init(self, compiler=None):
        self.compiler = compiler

    def process_IN_CREATE(self, event):
        self.compiler.add_path(event.pathname)

    def process_IN_DELETE(self, event):
        self.compiler.remove_path(event.pathname)

    def process_IN_MODIFY(self, event):
        self.compiler.add_path(event.pathname)

    def process_IN_MOVED_FROM(self, event):
        self.compiler.remove_path(event.pathname)

    def process_IN_MOVED_TO(self, event):
        self.compiler.add_path(event.pathname)


class Observer(BaseObserver):

    def __init__(self, source_dir, compiler):
        super(Observer, self).__init__(source_dir, compiler)
        wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(wm, default_proc_fun=Handler(compiler=compiler))
        mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_DELETE | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO
        wm.add_watch(source_dir, mask, rec=True, auto_add=True)

    def start(self):
        self.notifier.start()

    def stop(self):
        self.notifier.stop()
        self.compiler.terminate()