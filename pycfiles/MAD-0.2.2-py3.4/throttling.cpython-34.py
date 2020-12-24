# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\simulation\throttling.py
# Compiled at: 2016-04-27 04:07:37
# Size of source mod 2**32: 2954 bytes
from mad.evaluation import Symbols
from mad.simulation.commons import SimulatedEntity
from mad.simulation.tasks import TaskPoolDecorator

class ThrottlingPolicy(TaskPoolDecorator):
    __doc__ = '\n    Common interface of all throttling policies\n    '

    def __init__(self, task_pool):
        super().__init__(task_pool)

    def put(self, task):
        if self._accepts(task):
            self.delegate.put(task)
        else:
            task.reject()
            self._reject(task)

    def _accepts(self, task):
        raise NotImplementedError('Throttling:_accepts is abstract!')

    def _reject(self, task):
        task.reject()


class ThrottlingPolicyDecorator(ThrottlingPolicy):

    def __init__(self, delegate):
        super().__init__(delegate)
        self.delegate = delegate

    def _accepts(self, task):
        return self.delegate._accepts(task)

    def _reject(self, task):
        self.delegate._reject(task)


class NoThrottling(ThrottlingPolicy):
    __doc__ = '\n    Default policy: Always accept requests.\n    '

    def __init__(self, task_pool):
        super().__init__(task_pool)

    def _accepts(self, task):
        return True


class TailDrop(ThrottlingPolicy):
    __doc__ = '\n    Reject requests once the given task pool size reaches the\n    specified capacity\n    '
    NEGATIVE_CAPACITY = 'Capacity must be strictly positive, but found {capacity:d}'
    INVALID_CAPACITY = "Capacity must be an integer, but found '{object.__class__.__name__:s}'"

    def __init__(self, task_pool, capacity):
        super().__init__(task_pool)
        assert isinstance(capacity, int), self.INVALID_CAPACITY.format(object=capacity)
        assert capacity > 0, self.NEGATIVE_CAPACITY.format(capacity=capacity)
        self.capacity = capacity

    def _accepts(self, task):
        return self.delegate.size < self.capacity


class ThrottlingWrapper(SimulatedEntity, ThrottlingPolicyDecorator):

    def __init__(self, environment, task_pool):
        SimulatedEntity.__init__(self, Symbols.QUEUE, environment)
        ThrottlingPolicyDecorator.__init__(self, task_pool)

    def _reject(self, task):
        super()._reject(task)
        self.listener.rejection_of(task.request)