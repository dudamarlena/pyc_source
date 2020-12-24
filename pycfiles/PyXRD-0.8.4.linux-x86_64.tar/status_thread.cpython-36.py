# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/server/status_thread.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 688 bytes
import threading, time

class StatusThread(threading.Thread):

    def __init__(self, interval, provider):
        """
            @param interval: In seconds: how often to update the status.
        """
        assert interval > 0.1
        self.interval = interval
        self.stop_requested = threading.Event()
        self.provider = provider
        threading.Thread.__init__(self)

    def run(self):
        while not self.stop_requested.isSet():
            time.sleep(self.interval)
            self.provider._update_status(self.provider._get_status())

    def stop(self):
        self.stop_requested.set()
        self.join()