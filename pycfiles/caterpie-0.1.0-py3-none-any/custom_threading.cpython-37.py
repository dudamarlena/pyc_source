# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/custom_threading.py
# Compiled at: 2019-08-07 08:55:31
# Size of source mod 2**32: 1403 bytes
import threading
from .custom_queue import ThreadingQueue

class Thread(threading.Thread):

    def __init__(self, **kwargs):
        (super(Thread, self).__init__)(**kwargs)
        self._will_stop = False

    def stop(self):
        self._will_stop = True

    @property
    def will_stop(self):
        return self._will_stop


class ThreadPool:

    def __init__(self, link_instance, num_threads=1):
        self.link_instance = link_instance
        self.tasks_queue = ThreadingQueue()
        self.threads = []
        for i in range(num_threads):
            thread = Thread(target=(self._worker_target), args=[i])
            self.threads.append(thread)
            thread.start()

    def submit(self, target, args=None, kwargs=None):
        self.tasks_queue.put((target, args, kwargs))

    def _worker_target(self, i):
        while not self.threads[i].will_stop:
            try:
                target, args, kwargs = self.tasks_queue.get(timeout=1, block=False)
                if args:
                    target(*args)
                elif kwargs:
                    target(**kwargs)
                else:
                    target()
            except ThreadingQueue.EmptyError:
                pass
            except Exception:
                self.link_instance.logger.log('exception during the execution of a task', level='exception')