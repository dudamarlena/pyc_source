# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\simulation\service.py
# Compiled at: 2016-04-27 15:33:59
# Size of source mod 2**32: 4606 bytes
from mad.ast.actions import Think
from mad.evaluation import Symbols, Evaluation
from mad.simulation.commons import SimulatedEntity
from mad.simulation.workers import WorkerPool, Worker
from mad.simulation.tasks import Task

class Operation(SimulatedEntity):
    __doc__ = '\n    Represent an operation exposed by a service\n    '

    def __init__(self, name, parameters, body, environment):
        super().__init__(name, environment)
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return 'operation:%s' % str(self.body)

    def invoke(self, task, arguments, continuation=lambda r: r, worker=None):
        environment = self.environment.create_local_environment(worker.environment)
        environment.define(Symbols.TASK, task)
        environment.define_each(self.parameters, arguments)

        def compute_and_send_response(status):
            if task.request.kind == task.request.QUERY:
                return Evaluation(environment, Think(1), self.factory, lambda s: send_response(status)).result
            send_response(status)

        def send_response(status):
            if status.is_successful:
                if task.request.is_pending:
                    task.request.reply_success()
                    self.listener.success_replied_to(task.request)
                else:
                    self.listener.error_replied_to(task.request)
            elif status.is_erroneous:
                task.request.reply_error()
                self.listener.error_replied_to(task.request)
            service = environment.look_up(Symbols.SELF)
            worker = environment.dynamic_look_up(Symbols.WORKER)
            service.release(worker)
            continuation(status)

        return Evaluation(environment, self.body, self.factory, compute_and_send_response).result


class Service(SimulatedEntity):

    def __init__(self, name, environment):
        super().__init__(name, environment)
        self.environment.define(Symbols.SELF, self)
        self.environment.define(Symbols.SERVICE, self)
        self.tasks = self.environment.look_up(Symbols.QUEUE)
        self.workers = WorkerPool([self._new_worker(id) for id in range(1, 2)])

    def _new_worker(self, identifier):
        environment = self.environment.create_local_environment()
        environment.define(Symbols.SERVICE, self)
        return Worker(identifier, environment)

    @property
    def worker_count(self):
        return self.workers.capacity

    def set_worker_count(self, capacity):
        error = self.workers.capacity - capacity
        if error < 0:
            new_workers = [self._new_worker(id) for id in range(-error)]
            self.workers.add_workers(new_workers)
        elif error > 0:
            self.workers.shutdown(error)

    @property
    def utilisation(self):
        return self.workers.utilisation

    def process(self, request):
        self.listener.arrival_of(request)
        task = Task(request)
        if self.workers.are_available:
            request.accept()
            worker = self.workers.acquire_one()
            worker.assign(task)
        else:
            self.tasks.put(task)

    def release(self, worker):
        if self.tasks.are_pending:
            task = self.tasks.take()
            worker.assign(task)
        else:
            self.workers.release(worker)

    def activate(self, task):
        if self.workers.are_available:
            worker = self.workers.acquire_one()
            self.tasks.intercept(task)
            worker.assign(task)
        else:
            self.tasks.activate(task)

    def pause(self, task):
        self.tasks.pause(task)