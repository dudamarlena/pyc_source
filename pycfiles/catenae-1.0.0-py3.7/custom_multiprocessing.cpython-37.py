# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/custom_multiprocessing.py
# Compiled at: 2019-08-07 08:55:15
# Size of source mod 2**32: 1325 bytes
import multiprocessing

class Process(multiprocessing.Process):

    def __init__(self, **kwargs):
        (super(Process, self).__init__)(**kwargs)
        self._stop = multiprocessing.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()


class ProcessPool:

    def __init__(self, link_instance, num_processes=1):
        self.link_instance = link_instance
        self.tasks_queue = Queue()
        self.processes = []
        for i in range(num_processes):
            process = Process(target=(self._worker_target), args=[i])
            self.processes.append(process)
            process.start()

    def submit(self, target, args=None, kwargs=None):
        self.tasks_queue.put((target, args, kwargs))

    def _worker_target(self, i):
        while not self.processes[i].stopped():
            try:
                target, args, kwargs = self.tasks_queue.get()
                if args:
                    target(*args)
                else:
                    if kwargs:
                        target(**kwargs)
                    else:
                        target()
            except Exception:
                self.link_instance.logger.log(f'Exception during the execution of "{target.__name__}".',
                  level='exception')