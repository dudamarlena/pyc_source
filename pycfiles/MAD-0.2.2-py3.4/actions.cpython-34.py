# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\ast\actions.py
# Compiled at: 2016-04-24 15:38:04
# Size of source mod 2**32: 4544 bytes
from mad.ast.commons import Expression

class Action(Expression):
    __doc__ = '\n    Abstract all action that can be performed within an operation\n    '

    def __init__(self):
        super().__init__()

    def accept(self, evaluation):
        raise NotImplementedError('Action::accept(evaluation) is abstract!')


class Invocation(Action):
    __doc__ = '\n    Abstract invocation of a remote operation\n    '
    DEFAULT_PRIORITY = 5

    def __init__(self, service, operation, priority):
        super().__init__()
        self.service = service
        self.operation = operation
        self.priority = priority

    def accept(self, evaluation):
        raise NotImplementedError('Invocation::accept(evaluation) is abstract!')


class Trigger(Invocation):
    __doc__ = '\n    An non-blocking invocation of a remote operation\n    '

    def __init__(self, service, operation, priority=None):
        super().__init__(service, operation, priority or self.DEFAULT_PRIORITY)

    def accept(self, evaluation):
        return evaluation.of_trigger(self)

    def __repr__(self):
        return 'Trigger(%s, %s, %d)' % (self.service, self.operation, self.priority)


class Query(Invocation):
    __doc__ = '\n    A blocking invocation of a remote operation\n    '

    def __init__(self, service, operation, priority=None, timeout=None):
        super().__init__(service, operation, priority or self.DEFAULT_PRIORITY)
        self.timeout = timeout

    def accept(self, evaluation):
        return evaluation.of_query(self)

    @property
    def has_timeout(self):
        return self.timeout is not None

    def __repr__(self):
        return 'Query(%s, %s, %d)' % (self.service, self.operation, self.priority)


class Think(Action):
    __doc__ = '\n    Simulate a local time-consuming computation\n    '

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def accept(self, evaluation):
        return evaluation.of_think(self)

    def __repr__(self):
        return 'Think(%d)' % self.duration


class Fail(Action):
    __doc__ = '\n    Fail with a given probability\n    '
    NEGATIVE_PROBABILITY = 'Negative probability (found {0:5.2f})'

    def __init__(self, probability=1.0):
        super().__init__()
        assert probability >= 0.0, self.NEGATIVE_PROBABILITY.format(probability)
        self.probability = probability

    def accept(self, evaluation):
        return evaluation.of_fail(self)

    def __repr__(self):
        return 'Fail(%d)' % self.probability


class Delay(Expression):
    CONSTANT = 'constant'
    EXPONENTIAL = 'exponential'

    def __init__(self, base_delay=10, strategy=None):
        super().__init__()
        self.base_delay = base_delay
        self.strategy = strategy or self.CONSTANT


class Retry(Expression):
    __doc__ = '\n    Retry an action a given number of time\n    '
    DEFAULT_DELAY = Delay()

    def __init__(self, expression, limit=None, delay=None):
        super().__init__()
        self.expression = expression
        if not not limit:
            assert limit > 0, 'Retry limit must be strictly positive (found %d)' % limit
        self.limit = limit
        self.delay = delay or self.DEFAULT_DELAY

    def accept(self, evaluation):
        return evaluation.of_retry(self)

    def __repr__(self):
        return 'Retry(%s, %d)' % (str(self.expression), self.limit)


class IgnoreError(Expression):
    __doc__ = '\n    Ignore error occuring during the evaluation of the given expression\n    '

    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def accept(self, evaluation):
        return evaluation.of_ignore_error(self)

    def __repr__(self):
        return 'IgnoreError(%s)' % str(self.expression)