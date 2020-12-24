# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/diwnotifier/utils/threads_collector.py
# Compiled at: 2014-01-29 20:11:34
import threading

class ThreadsCollector(object):

    def __init__(self, *jobs):
        self.jobs = jobs
        self.threads = []

    def make(self):
        for job in self.jobs:
            thread = threading.Thread(target=job)
            self.threads.append(thread)

    def start_all(self):
        for thread in self.threads:
            thread.start()

    def join_all(self):
        for thread in self.threads:
            thread.join()

    def clean_all(self):
        del self.threads[:]