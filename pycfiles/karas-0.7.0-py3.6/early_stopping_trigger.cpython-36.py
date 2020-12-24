# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/triggers/early_stopping_trigger.py
# Compiled at: 2019-01-18 09:08:10
# Size of source mod 2**32: 2324 bytes
import operator, warnings
from karas import compare_key
from karas.training.triggers.utils import get_trigger

class EarlyStoppingTrigger(object):

    def __init__(self, check_trigger=(1, 'epoch'), monitor='main/loss', patients=3, mode='auto', verbose=True, max_trigger=(100, 'epoch')):
        self.count = 0
        self.monitor = monitor
        self.patients = patients
        self.verbose = verbose
        self.max_trigger = get_trigger(max_trigger)
        self.interval_trigger = get_trigger(check_trigger)
        if mode == 'min':
            self.compare = operator.lt
        else:
            if mode == 'max':
                self.compare = operator.gt
            else:
                if 'accuracy' in monitor:
                    self.compare = operator.gt
                else:
                    self.compare = operator.lt
            if self.compare == operator.gt:
                if self.verbose:
                    print('early stopping: operator is greater')
                self.best = float('-inf')
            else:
                if self.verbose:
                    print('early stopping: operator is less')
                self.best = float('inf')

    def __call__(self, trainer):
        observation = trainer.reporter.observation
        if self.max_trigger(trainer):
            return True
        find_key = False
        for tag, value in observation.items():
            if compare_key(self.monitor, tag):
                find_key = True
                break

        if not find_key:
            if self.verbose:
                warnings.warn('{} is not in observation'.format(self.monitor))
            return False
        if not self.interval_trigger(trainer):
            return False
        else:
            for tag, value in observation.items():
                if compare_key(self.monitor, tag):
                    current_val = value

            if self.compare(current_val, self.best):
                self.best = current_val
                self.count = 0
            else:
                self.count += 1
            if self._stop_condition():
                if self.verbose:
                    print('Epoch {}: early stopping'.format(trainer.epoch))
                return True
            return False

    def _stop_condition(self):
        return self.count >= self.patients

    def get_training_length(self):
        return self.max_trigger.get_training_length()