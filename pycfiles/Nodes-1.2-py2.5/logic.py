# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/logic.py
# Compiled at: 2009-09-13 12:51:27
"""Node-like logic."""
from core import Node

class EqMixin:

    @staticmethod
    def truth(a, b):
        return a == b


class LtMixin:

    @staticmethod
    def truth(a, b):
        return a < b


class GtMixin:

    @staticmethod
    def truth(a, b):
        return a > b


class NeMixin:

    @staticmethod
    def truth(a, b):
        return a != b


class ComparisionSelect(Node):
    """If truth(a, b) then a else b."""
    __shape__ = (
     [
      'val a', 'val b'], ['val c res'])

    def calculate(self):
        if self.truth(*map(round, self.input)):
            self.output[0] = self.input[0]
        else:
            self.output[0] = self.input[1]

    @staticmethod
    def truth(a, b):
        raise NotImplementedError, 'method .truth must be implemented in subclasses.'


class EqSelect(EqMixin, ComparisionSelect):
    pass


class LtSelect(LtMixin, ComparisionSelect):
    pass


class GtSelect(GtMixin, ComparisionSelect):
    pass


class NeSelect(NeMixin, ComparisionSelect):
    pass


class ComparisionBoolean(Node):
    """If truth(a, b) then 1 else 0."""
    __shape__ = (
     [
      'val a', 'val b'], ['val bool c res'])

    def calculate(self):
        if self.truth(*map(round, self.input)):
            self.output[0] = 1
        else:
            self.output[0] = 0

    @staticmethod
    def truth(a, b):
        raise NotImplementedError, 'method .truth must be implemented in subclasses.'


class EqBoolean(EqMixin, ComparisionBoolean):
    pass


class LtBoolean(LtMixin, ComparisionBoolean):
    pass


class GtBoolean(GtMixin, ComparisionBoolean):
    pass


class NeBoolean(NeMixin, ComparisionBoolean):
    pass


class BooleanOperation(Node):
    __shape__ = (
     [
      'val bool a', 'val bool b'], ['val bool c res'])

    def calculate(self):
        a = round(self.input[0])
        b = round(self.input[1])
        self.output[0] = int(self.truth(a, b))

    @staticmethod
    def truth():
        raise NotImplementedError, 'method .truth must be implemented in subclasses.'


class AndBoolean(BooleanOperation):

    @staticmethod
    def truth(a, b):
        return a and b


class OrBoolean(BooleanOperation):

    @staticmethod
    def truth(a, b):
        return a or b


class NotBoolean(BooleanOperation):
    __shape__ = (
     [
      'val bool a'], ['val bool b res'])

    def calculate(self):
        a = round(self.input[0])
        self.output[0] = int(self.truth(a))

    @staticmethod
    def truth(a):
        return not a


class Boolean(NotBoolean):

    @staticmethod
    def truth(a):
        return not not a