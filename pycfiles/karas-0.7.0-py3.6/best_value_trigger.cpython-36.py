# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/triggers/best_value_trigger.py
# Compiled at: 2019-01-15 03:50:21
# Size of source mod 2**32: 1406 bytes
import operator, karas.reporter as reporter
from karas import compare_key
from karas.training.triggers import utils

class BestValueTrigger(object):

    def __init__(self, key, compare, trigger=(1, 'epoch')):
        self.key = key
        self.best_value = None
        self.interval_trigger = utils.get_trigger(trigger)
        self.compare = compare
        self._init_summary()

    def __call__(self, trainer):
        observation = trainer.observation
        summary = self._summary
        for key in observation.keys():
            if compare_key(self.key, key):
                summary.add({self.key: observation[key]})

        if not self.interval_trigger(trainer):
            return False
        else:
            stats = summary.compute_mean()
            value = float(stats[self.key])
            self._init_summary()
            if self.best_value is None or self.compare(self.best_value, value):
                self.best_value = value
                return True
            return False

    def _init_summary(self):
        self._summary = reporter.DictSummary()


class MaxValueTrigger(BestValueTrigger):

    def __init__(self, key, trigger=(1, 'epoch')):
        super(MaxValueTrigger, self).__init__(key, operator.gt, trigger)


class MinValueTrigger(BestValueTrigger):

    def __init__(self, key, trigger=(1, 'epoch')):
        super(MinValueTrigger, self).__init__(key, operator.lt, trigger)