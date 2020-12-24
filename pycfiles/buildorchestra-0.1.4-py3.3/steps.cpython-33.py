# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buildorchestra/steps.py
# Compiled at: 2016-10-05 09:42:50
# Size of source mod 2**32: 1044 bytes
from abc import ABCMeta, abstractmethod

class Step(metaclass=ABCMeta):

    @property
    @abstractmethod
    def identifier(self):
        pass

    @property
    @abstractmethod
    def shouldExecute(self):
        True

    @abstractmethod
    def execute(self, **options):
        pass

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __lt__(self, other):
        return self.identifier < other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def __repr__(self):
        return self.identifier


class BuildStep(Step):

    def __init__(self, identifier, method):
        self._identifier = identifier
        self._method = method

    @property
    def identifier(self):
        return self._identifier

    @property
    def shouldExecute(self):
        return True

    def execute(self, **options):
        return self._method(**options)


class TargetStep(Step):

    def __init__(self, identifier):
        self._identifier = identifier

    @property
    def identifier(self):
        return self._identifier

    @property
    def shouldExecute(self):
        return False

    def execute(self, **options):
        pass