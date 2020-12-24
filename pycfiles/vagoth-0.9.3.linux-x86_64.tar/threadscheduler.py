# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/scheduler/threadscheduler.py
# Compiled at: 2013-02-09 06:59:34
from threading import Thread
from Queue import Queue

class Worker(object):
    """
    Worker class for `ThreadScheduler`
    """

    def __init__(self, manager):
        self.manager = manager
        self.queue = Queue()

    def run(self):
        while True:
            action, kwargs = self.queue.get()
            if action is None:
                break
            try:
                self.manager.action(action, **kwargs)
            except Exception as e:
                print e

        return

    def stop(self):
        """Signal to the thread that it should quit"""
        self.queue.put((None, None))
        return

    def action(self, action, **kwargs):
        """Add an action to the queue"""
        self.queue.put((action, kwargs))


class ThreadScheduler(object):
    """
    Runs a single worker in a Thread to process
    all actions in the background.
    """

    def __init__(self, manager, config):
        self.manager = manager
        self.config = config
        self.worker = Worker(manager)
        self.thread = Thread(target=self.worker.run)
        self.thread.start()

    def action(self, queue_name, action, **kwargs):
        """Schedule the specified action, ignoring queue_name"""
        self.worker.action(action, **kwargs)

    def cleanup(self):
        """Request the worker thread to exit"""
        self.worker.stop()