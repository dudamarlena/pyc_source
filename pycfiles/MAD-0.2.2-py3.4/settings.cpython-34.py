# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\ast\settings.py
# Compiled at: 2016-04-26 15:24:25
# Size of source mod 2**32: 2996 bytes
from mad.ast.commons import Expression

class NoThrottlingSettings(Expression):
    __doc__ = '\n    Configuration of a "no throttling" policy\n    '

    def __init__(self):
        super().__init__()

    def accept(self, evaluation):
        return evaluation.of_no_throttling(self)


class TailDropSettings(Expression):
    __doc__ = '\n    Configuration of a "tail drop" throttling policy\n    '

    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity

    def accept(self, evaluation):
        return evaluation.of_tail_drop(self)


class QueueDiscipline(Expression):

    def __init__(self):
        super().__init__()

    def accept(self, evaluation):
        raise NotImplementedError('QueueDiscipline::accept is abstract!')


class LIFO(QueueDiscipline):

    def __init__(self):
        super().__init__()

    def accept(self, evaluation):
        return evaluation.of_lifo(self)

    def __repr__(self):
        return 'LIFO'


class FIFO(QueueDiscipline):

    def accept(self, evaluation):
        return evaluation.of_fifo(self)

    def __repr__(self):
        return 'FIFO'


class Autoscaling(Expression):

    def __init__(self, period=30, limits=(1, 1)):
        super().__init__()
        if not isinstance(period, int):
            raise ValueError("Expecting integer value for period, but found '%1$s' (%2$s)" % (str(period), type(period)))
        self.period = period
        if not isinstance(limits, tuple):
            raise ValueError("Expecting interval (min, max) for limits but found '%1$s'" % str(limits))
        self.limits = limits

    def accept(self, evaluation):
        return evaluation.of_autoscaling(self)

    def __repr__(self):
        return 'Autoscaling(%1$d, %2$s)' % (self.period, str(self.limits))


class Settings(Expression):

    def __init__(self, queue=None, autoscaling=None, throttling=None):
        super().__init__()
        self.queue = queue or FIFO()
        self.autoscaling = autoscaling or Autoscaling()
        self.throttling = throttling or NoThrottlingSettings()

    def accept(self, evaluation):
        return evaluation.of_settings(self)

    def __repr__(self):
        return 'Settings(queue: %s)' % str(self._queue)