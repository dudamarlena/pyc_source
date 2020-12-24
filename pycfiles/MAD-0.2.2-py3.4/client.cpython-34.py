# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\simulation\client.py
# Compiled at: 2016-04-26 09:26:41
# Size of source mod 2**32: 2211 bytes
from mad.evaluation import Symbols, Evaluation
from mad.simulation.commons import SimulatedEntity
from mad.simulation.tasks import Task

class Monitor:

    def __init__(self):
        self.success_count = 0
        self.error_count = 0

    def record_success(self):
        self.success_count += 1

    def record_error(self):
        self.error_count += 1


class ClientStub(SimulatedEntity):

    def __init__(self, name, environment, period, body):
        super().__init__(name, environment)
        self.environment.define(Symbols.SELF, self)
        self.period = period
        self.body = body
        self.monitor = Monitor()

    def initialize(self):
        self.schedule.every(self.period, self.invoke)

    def invoke(self):

        def post_processing(result):
            if result.is_successful:
                self.on_success()
            elif result.is_erroneous:
                self.on_error()

        self.environment.define(Symbols.TASK, Task())
        env = self.environment.create_local_environment(self.environment)
        env.define(Symbols.WORKER, self)
        Evaluation(env, self.body, self.factory, post_processing).result

    def activate(self, task):
        task.resume(self)

    def pause(self, task):
        pass

    def release(self, worker):
        pass

    def on_success(self):
        self.monitor.record_success()

    def on_error(self):
        self.monitor.record_error()