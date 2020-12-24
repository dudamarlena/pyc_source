# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\simulation\workers.py
# Compiled at: 2016-04-27 08:03:11
# Size of source mod 2**32: 3661 bytes
from mad.evaluation import Symbols
from mad.simulation.commons import SimulatedEntity

class WorkerPool:
    __doc__ = '\n    Represent a pool of workers that can take over a simple task\n    '

    def __init__(self, workers):
        assert len(workers) > 0, 'Cannot build a worker pool without any worker!'
        self.idle_workers = workers
        self.busy_workers = []
        self.stopped_workers = []

    @property
    def capacity(self):
        return len(self.idle_workers) + len(self.busy_workers)

    def add_workers(self, new_workers):
        assert len(new_workers) > 0, 'Cannot add empty list of workers!'
        self.idle_workers.extend(new_workers)

    def shutdown(self, count):
        assert count < self.capacity, 'Invalid shutdown %d (capacity %d)' % (count, self.capacity)
        for index in range(count):
            if len(self.idle_workers) > 0:
                self.idle_workers.pop(0)
            else:
                assert len(self.busy_workers) > 0
                stopped_worker = self.busy_workers.pop(0)
                self.stopped_workers.append(stopped_worker)

    @property
    def utilisation(self):
        return 100 * (1 - len(self.idle_workers) / self.capacity)

    @property
    def idle_worker_count(self):
        return len(self.idle_workers)

    @property
    def are_available(self):
        return len(self.idle_workers) > 0

    def acquire_one(self):
        if not self.are_available:
            raise ValueError('Cannot acquire from an empty worker pool!')
        busy_worker = self.idle_workers.pop(0)
        self.busy_workers.append(busy_worker)
        return busy_worker

    def release(self, worker):
        assert worker not in self.idle_workers, 'Error: Cannot release an idle worker!'
        if worker in self.busy_workers:
            self.idle_workers.append(worker)
            self.busy_workers.remove(worker)
        else:
            assert worker in self.stopped_workers, 'Error: Unknown worker (not idle, not busy, not stopped)!'
            self.stopped_workers.remove(worker)


class Worker(SimulatedEntity):
    __doc__ = '\n    Represent a worker (i.e., a thread, or a service replica) that handles requests\n    '

    def __init__(self, identifier, environment):
        super().__init__('Worker %d' % identifier, environment)
        self.environment.define(Symbols.WORKER, self)
        self.identifier = identifier

    def assign(self, task):
        if task.request.is_pending:
            if task.is_started:
                task.resume(self)
            else:
                task.mark_as_started()
                operation = self.look_up(task.request.operation)
                operation.invoke(task, [], worker=self)
        else:
            self.listener.error_replied_to(task.request)