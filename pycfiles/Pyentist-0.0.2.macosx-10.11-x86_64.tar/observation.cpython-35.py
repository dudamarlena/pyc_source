# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mpcabd/Projects/pyentist/env/lib/python3.5/site-packages/pyentist/observation.py
# Compiled at: 2016-03-06 14:35:05
# Size of source mod 2**32: 1804 bytes
import time

class Observation(object):

    def __init__(self, name, experiment, callback):
        self.name = name
        self.experiment = experiment
        self.callback = callback
        self.now = time.time()
        try:
            self._returned_value = self.callback()
        except Exception as e:
            self._raised_exception = e

        self.duration = time.time() - self.now

    def __hash__(self):
        return sum(map(hash, [self.returned_value, self.raised_exception, self.__class__]))

    def is_equivalent_to(self, other, comparer=None):
        if not isinstance(other, Observation):
            return False
        values_are_equal = False
        both_raised = self.raised_exception and other.raised_exception
        neither_raised = not self.raised_exception and not other.raised_exception
        if neither_raised:
            if comparer:
                values_are_equal = comparer(self.returned_value, other.returned_value)
            else:
                values_are_equal = self.returned_value == other.returned_value
            return values_are_equal
        if both_raised:
            return self.raised_exception.__class__ == other.raised_exception.__class__ and str(self.raised_exception) == str(other.raised_exception)
        return False

    @property
    def raised_exception(self):
        if not hasattr(self, '_raised_exception'):
            return
        return self._raised_exception

    @property
    def returned_value(self):
        if not hasattr(self, '_returned_value'):
            return
        return self._returned_value

    @property
    def cleaned_value(self):
        if self.returned_value:
            return self.experiment.clean_value(self.returned_value)