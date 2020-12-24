# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/service/mixins/daemon.py
# Compiled at: 2015-11-10 04:27:34
from threading import Thread
import signal
threads = []

def stop_daemons(signal, action):
    global threads
    for thread in threads:
        thread.cleanup()


signal.signal(signal.SIGTERM, stop_daemons)
signal.signal(signal.SIGINT, stop_daemons)

class DaemonMixin(Thread):
    i_am_running = True

    def run(self):
        pass

    def _start_daemon(self, background=False):
        threads.append(self)
        if background:
            self.start()
        else:
            self.run()

    def cleanup(self):
        self.i_am_running = False
        super(DaemonMixin, self).cleanup()