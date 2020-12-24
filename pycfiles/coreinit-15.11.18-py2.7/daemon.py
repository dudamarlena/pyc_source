# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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