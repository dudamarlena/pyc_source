# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danvk/github/dpxdt/dpxdt/client/timer_worker.py
# Compiled at: 2014-07-24 17:15:00
"""Workers for driving screen captures, perceptual diffs, and related work."""
import Queue, heapq, logging, time, gflags
FLAGS = gflags.FLAGS
from dpxdt.client import workers

class TimerItem(workers.WorkItem):
    """Work item for waiting some period of time before returning."""

    def __init__(self, delay_seconds):
        workers.WorkItem.__init__(self)
        self.delay_seconds = delay_seconds
        self.ready_time = time.time() + delay_seconds


class TimerThread(workers.WorkerThread):
    """"Worker thread that tracks many timers."""

    def __init__(self, *args):
        """Initializer."""
        workers.WorkerThread.__init__(self, *args)
        self.timers = []

    def handle_nothing(self):
        now = time.time()
        while self.timers:
            ready_time, _ = self.timers[0]
            wait_time = ready_time - now
            if wait_time <= 0:
                _, item = heapq.heappop(self.timers)
                self.output_queue.put(item)
            else:
                self.polltime = wait_time
                return

        self.polltime = FLAGS.polltime

    def handle_item(self, item):
        heapq.heappush(self.timers, (item.ready_time, item))
        self.handle_nothing()


def register(coordinator):
    """Registers this module as a worker with the given coordinator."""
    timer_queue = Queue.Queue()
    coordinator.register(TimerItem, timer_queue)
    coordinator.worker_threads.append(TimerThread(timer_queue, coordinator.input_queue))