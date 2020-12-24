# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/fakeProcess.py
# Compiled at: 2013-09-24 00:56:56
import time

def cpu_count():
    return 1


class Process:

    def __init__(self):
        self.pid = int(round(time.time()))
        self.exitcode = None
        return

    def start(self):
        self.run()

    def run(self):
        pass

    def join(self):
        pass


class Manager:

    def dict(self):
        return dict()