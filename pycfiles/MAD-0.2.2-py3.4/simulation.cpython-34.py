# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\simulation.py
# Compiled at: 2016-04-20 14:55:11
# Size of source mod 2**32: 18197 bytes
from mad.ast import Settings
from mad.environment import Environment
from mad.scheduling import Scheduler
from mad.simulation.autoscaling import RuleBasedStrategy

class Symbols:
    AUTOSCALING = '!autoscaling'
    SIMULATION = '!simulation'
    SELF = '!self'
    TASK = '!request'
    SERVICE = '!service'
    WORKER = '!worker'
    QUEUE = '!queue'


class Evaluation:
    __doc__ = '\n    Represent the future evaluation of an expression, within a given environment. The expression is bound to\n    a continuation, that is the next evaluation to carry out.\n    '

    def __init__(self, environment, expression, continuation=lambda x: x):
        self.environment = environment
        self.expression = expression
        assert callable(continuation), 'Continuations must be callable!'
        self.continuation = continuation
        self.simulation = self.environment.look_up(Symbols.SIMULATION)

    def _look_up(self, symbol):
        return self.environment.look_up(symbol)

    def _define(self, symbol, value):
        self.environment.define(symbol, value)

    def _evaluation_of(self, expression, continuation=lambda x: None):
        return Evaluation(self.environment, expression, continuation).result

    @property
    def result(self):
        return self.expression._accepts(self)

    def of_service_definition(self, service):
        service_environment = self.environment.create_local_environment()
        Evaluation(service_environment, Settings()).result
        Evaluation(service_environment, service.body).result
        service = Service(service.name, service_environment)
        self._define(service.name, service)
        return self.continuation(Success(service))

    def of_settings(self, settings):
        self._evaluation_of(settings.queue)
        self._evaluation_of(settings._autoscaling)
        return self.continuation(Success(None))

    def of_fifo(self, fifo):
        self._define(Symbols.QUEUE, FIFOTaskPool())
        return self.continuation(Success(None))

    def of_lifo(self, lifo):
        self._define(Symbols.QUEUE, LIFOTaskPool())
        return self.continuation(Success(None))

    def of_autoscaling(self, autoscaling):
        strategy = RuleBasedStrategy(autoscaling.limits[0], autoscaling.limits[1], 70, 80)
        autoscaler = AutoScaler(self.environment, autoscaling.period, strategy)
        self._define(Symbols.AUTOSCALING, autoscaler)
        return self.continuation(Success(None))

    def of_operation_definition(self, definition):
        operation = Operation(definition.name, definition.parameters, definition.body, self.environment)
        self.environment.define(definition.name, operation)
        return self.continuation(Success(operation))

    def of_client_stub_definition(self, definition):
        client_environment = self.environment.create_local_environment()
        client = ClientStub(definition.name, client_environment, definition.period, definition.body)
        self._define(definition.name, client)
        client.initialize()
        return self.continuation(Success(client))

    def of_sequence(self, sequence):

        def abort_on_error(previous):
            if previous.is_successful:
                return self._evaluation_of(sequence.rest, self.continuation)
            else:
                return self.continuation(previous)

        return self._evaluation_of(sequence.first_expression, abort_on_error)

    def of_trigger(self, trigger):
        sender = self._look_up(Symbols.SELF)
        recipient = self._look_up(trigger.service)
        Request(sender, trigger.operation).send_to(recipient)
        return self.continuation(Success(None))

    def of_query(self, query):
        task = self._look_up(Symbols.TASK)
        sender = self._look_up(Symbols.SELF)
        recipient = self._look_up(query.service)

        def on_success():
            sender.log('Req. %d complete', request.identifier)

            def resume(worker):
                self.environment.dynamic_scope = worker.environment
                self.continuation(Success())

            task.resume = resume
            sender.activate(task)

        def on_error():
            sender.log('Req. %d failed', request.identifier)

            def resume(worker):
                self.environment.dynamic_scope = worker.environment
                self.continuation(Error())

            task.resume = resume
            sender.activate(task)

        request = Request(sender, query.operation, on_success, on_error)
        sender.log('Sending Req. %d to %s::%s', (request.identifier, query.service, query.operation))
        request.send_to(recipient)
        worker = self.environment.dynamic_look_up(Symbols.WORKER)
        sender.release(worker)
        return Success(None)

    def of_think(self, think):

        def resume():
            self.continuation(Success())

        self.simulation.schedule.after(think.duration, resume)
        return Success()

    def of_retry(self, retry):

        def do_retry(remaining_tries):
            if remaining_tries == 0:
                return lambda status: Error()

            def continuation(status):
                if status.is_successful:
                    return self.continuation(status)
                else:
                    return self._evaluation_of(retry.expression, do_retry(remaining_tries - 1))

            return continuation

        return self._evaluation_of(retry.expression, do_retry(retry.limit - 1))

    def of_ignore_error(self, ignore_error):

        def ignore_status(status):
            return self.continuation(Success(status.value))

        return self._evaluation_of(ignore_error.expression, ignore_status)


class Result:
    __doc__ = '\n    Represent the result of an evaluation, including the status (pass, failed) and the value if associated value if any\n    '
    SUCCESS = 1
    ERROR = 2

    def __init__(self, status, value):
        self.status = status
        self.value = value

    @property
    def is_successful(self):
        return self.status == Result.SUCCESS

    def __repr__(self):
        if self.is_successful:
            return 'SUCCESS'
        return 'ERROR'


class Success(Result):

    def __init__(self, value=None):
        super().__init__(Result.SUCCESS, value)


class Error(Result):

    def __init__(self):
        super().__init__(Result.ERROR, None)


class Simulation:
    __doc__ = '\n    Represent the general simulation, including the current schedule and the associated trace\n    '

    def __init__(self, log, report_factory):
        self._scheduler = Scheduler()
        self.log = log
        self.reports = report_factory
        self.environment = Environment()
        self.environment.define(Symbols.SIMULATION, self)
        self._next_request_id = 1

    def run_until(self, end, display=None):
        self._scheduler.simulate_until(end, display)

    @property
    def schedule(self):
        return self._scheduler

    def evaluate(self, expression):
        return Evaluation(self.environment, expression).result

    def next_request_id(self):
        id = self._next_request_id
        self._next_request_id += 1
        return id

    @property
    def services(self):
        return self._find_by_type(Service)

    @property
    def clients(self):
        return self._find_by_type(ClientStub)

    def _find_by_type(self, type):
        return [each_value for each_value in self.environment.bindings.values() if isinstance(each_value, type)]


class SimulatedEntity:
    __doc__ = '\n    Factor out commonalities between all simulated entities\n    '

    def __init__(self, name, environment):
        self.environment = environment
        self.name = name
        self.simulation = self.environment.look_up(Symbols.SIMULATION)

    @property
    def schedule(self):
        return self.simulation.schedule

    def log(self, message, values):
        now = self.schedule.time_now
        caller = self.look_up(Symbols.SELF)
        self.simulation.log.record(now, caller.name, message % values)

    def look_up(self, symbol):
        return self.environment.look_up(symbol)


class AutoScaler(SimulatedEntity):
    __doc__ = '\n    Autoscaler periodically recomputes the number of worker for service in its logical scope.\n    '
    NAME = '!Autoscaler'

    def __init__(self, environment, period, strategy):
        super().__init__(self.NAME, environment)
        self.period = period
        self.schedule.every(period, self.auto_scale)
        self.strategy = strategy

    def auto_scale(self):
        service = self.look_up(Symbols.SERVICE)
        self.strategy.adjust(service)


class Service(SimulatedEntity):
    MONITORING_PERIOD = 10

    def __init__(self, name, environment):
        super().__init__(name, environment)
        self.environment.define(Symbols.SELF, self)
        self.environment.define(Symbols.SERVICE, self)
        self.tasks = self.environment.look_up(Symbols.QUEUE)
        self.workers = WorkerPool([self._new_worker(id) for id in range(1, 2)])
        self.schedule.every(self.MONITORING_PERIOD, self.monitor)

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
            new_workers = [self._new_worker(id) for id in range(self.workers.capacity, capacity + 1)]
            self.workers.add_workers(new_workers)
        elif error > 0:
            self.workers.shutdown(error)

    @property
    def utilisation(self):
        return self.workers.utilisation

    def process(self, request):
        task = Task(request)
        if self.workers.are_available:
            self.log('Req. %d accepted', request.identifier)
            worker = self.workers.acquire_one()
            worker.assign(task)
        else:
            self.log('Req. %d enqueued', request.identifier)
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
            worker.assign(task)
        else:
            self.tasks.activate(task)

    def monitor(self):
        report = self.simulation.reports.report_for_service(self.name)
        report(time=self.schedule.time_now, queue_length=self.tasks.size, utilisation=self.workers.utilisation, worker_count=self.worker_count)


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

        def send_response(status):
            self.log('Reply to Req. %d (%s)', (task.request.identifier, str(status)))
            if status.is_successful:
                task.request.reply_success()
            else:
                task.request.reply_error(status)
            continuation(status)

        Evaluation(environment, self.body, send_response).result


class WorkerPool:

    def __init__(self, workers):
        assert len(workers) > 0, 'Cannot build a worker pool without any worker!'
        self.capacity = len(workers)
        self.idle_workers = workers

    def add_workers(self, new_workers):
        assert len(new_workers) > 0, 'Cannot add empty list of workers!'
        self.idle_workers.extend(new_workers)
        self.capacity += len(new_workers)

    def shutdown(self, count):
        assert count < self.capacity, 'Invalid shutdown %d (capacity %d)' % (count, self.capacity)
        self.capacity -= count
        for index in range(min(len(self.idle_workers), count)):
            self.idle_workers.pop(0)

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
        return self.idle_workers.pop(0)

    def release(self, worker):
        if len(self.idle_workers) < self.capacity:
            self.idle_workers.append(worker)


class Worker(SimulatedEntity):
    __doc__ = '\n    Represent a worker (i.e., a thread, or a service replica) that handles requests\n    '

    def __init__(self, identifier, environment):
        super().__init__('Worker %d' % identifier, environment)
        self.environment.define(Symbols.WORKER, self)
        self.identifier = identifier

    def assign(self, task):

        def release_worker(result):
            service = self.look_up(Symbols.SERVICE)
            service.release(self)

        if task.is_started:
            task.resume(self)
        else:
            task.mark_as_started()
            operation = self.look_up(task.request.operation)
            operation.invoke(task, [], release_worker, self)


class TaskPool:

    def __init__(self):
        self.requests = []

    def put(self, request):
        self.requests.append(request)

    def take(self):
        raise NotImplementedError('TaskPool::take is abstract!')

    @property
    def is_empty(self):
        return self.size == 0

    @property
    def are_pending(self):
        return not self.is_empty

    @property
    def size(self):
        return len(self.requests)

    def activate(self, request):
        raise NotImplementedError('TaskPool::activate is abstract!')


class FIFOTaskPool(TaskPool):

    def __init__(self):
        super().__init__()

    def take(self):
        if self.is_empty:
            raise ValueError('Cannot take a request from an empty pool!')
        return self.requests.pop(0)

    def activate(self, request):
        self.requests.insert(0, request)


class LIFOTaskPool(TaskPool):

    def __init__(self):
        super().__init__()

    def take(self):
        if self.is_empty:
            raise ValueError('Cannot take a request from an empty pool!')
        return self.requests.pop(-1)

    def activate(self, request):
        self.requests.append(request)


class Task:

    def __init__(self, request=None):
        self.request = request
        self.is_started = False
        self.resume = lambda : None

    def mark_as_started(self):
        self.is_started = True


class ClientStub(SimulatedEntity):

    def __init__(self, name, environment, period, body):
        super().__init__(name, environment)
        self.environment.define(Symbols.SELF, self)
        self.period = period
        self.body = body

    def initialize(self):
        self.schedule.every(self.period, self.invoke)

    def invoke(self):

        def post_processing(status):
            if status.is_successful:
                self.on_success()
            else:
                self.on_error()

        self.environment.define(Symbols.TASK, Task())
        env = self.environment.create_local_environment(self.environment)
        env.define(Symbols.WORKER, self)
        Evaluation(env, self.body, post_processing).result

    def activate(self, task):
        task.resume(self)

    def release(self, worker):
        pass

    def on_success(self):
        pass

    def on_error(self):
        pass


class Status:
    SUCCESS = 1
    ERROR = 2
    WAITING = 3


class Request:

    def __init__(self, sender, operation, on_success=lambda : None, on_error=lambda : None):
        assert sender, 'Invalid sender (found %s)' % str(sender)
        self.identifier = sender.simulation.next_request_id()
        self.sender = sender
        self.operation = operation
        self.on_success = on_success
        self.on_error = on_error

    def send_to(self, service):
        service.process(self)

    def reply_success(self):
        self.on_success()

    def reply_error(self):
        self.on_error()