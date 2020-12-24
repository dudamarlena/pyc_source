# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/basic.py
# Compiled at: 2009-09-27 01:21:21
"""Basic Node types."""
from core import Node, Stop, array

class GeneralizedNeuron(Node):
    __shape__ = (
     [
      '', None], ['', None])

    def calculate(self):
        x = sum(self.input) / self.iN
        self.output[:] = x

    def calc_drv(self, value):
        return 1 / self.iN


class StandardNeuron(GeneralizedNeuron):
    __shape__ = (
     [
      '', None], [''])


class DistributorNeuron(GeneralizedNeuron):
    __shape__ = (
     [
      ''], ['', None])


class InputMemory(Node):
    __shape__ = ([], [None])

    def init_prepare(self):
        Node.init_prepare(self)
        self.common_weight = 1

    def set(self, value):
        self.value = value

    def calculate(self):
        self.output[:] = self.value * self.common_weight

    def back_propagation(self, targets):
        assert len(targets) == self.oN
        targets = array(targets)
        delta = (targets - self.ovalues) / self.output_weights * self.common_weight
        self.common_weight += sum(delta) * self.value * self.velocity


class OutputMemory(Node):
    __shape__ = (
     [
      None], [])

    def init_prepare(self):
        Node.init_prepare(self)
        self.common_weight = 1

    def get(self):
        return self.value

    def calculate(self):
        self.value = sum(self.input) / self.iN * self.common_weight

    def check_sufficient(self, getted, values):
        return True

    def back_propagation(self, target):
        try:
            target = target[0]
        except (IndexError, TypeError):
            pass

        d = (target - self.value) * self.common_weight
        self.input_weights += d * self.ivalues * self.velocity
        map(lambda x, y: x.back_propagate(d * y), self.inputs, self.input_weights)


class AssociativeMemory(Node):
    __shape__ = (
     [
      'control', 'key'], ['value'])

    def init_prepare(self):
        Node.init_prepare(self)
        self.key = self.value = 0

    def check_sufficient(self, getted, values):
        return getted[1] or getted[0] and round(values[0]) == self.key

    def calculate(self):
        if self.input[1]:
            self.value = self.input[1]
            raise Stop
        elif round(self.input[0]) == self.key:
            self.output[0] = self.value
        else:
            raise Stop

    def set(self, key, value=0):
        self.key = key
        self.value = value

    def __getstate_extra__(self):
        return (
         self.key, self.value)

    def __setstate_extra__(self, state):
        (self.key, self.value) = state