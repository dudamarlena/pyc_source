# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unbound_ec2/repeater.py
# Compiled at: 2016-11-14 04:03:05
import threading

class RecursiveRepeater(threading.Thread):
    """Periodically runs code in a thread.
    """

    def __init__(self, delay, callme):
        """Calls `callme`  every  `delay` seconds.
        """
        threading.Thread.__init__(self)
        self.callme = callme
        self.delay = delay
        self.event = threading.Event()
        self.daemon = True

    def run(self):
        while not self.event.wait(1.0):
            self.callme()
            self.event.wait(self.delay)

    def stop(self):
        self.event.set()
        self.join()