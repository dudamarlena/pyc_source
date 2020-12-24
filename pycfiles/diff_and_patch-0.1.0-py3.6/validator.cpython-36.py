# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/diff_and_patch/validator.py
# Compiled at: 2018-08-26 08:44:11
# Size of source mod 2**32: 883 bytes
import abc
from collections import defaultdict
from diff_and_patch.utils import fully_qualified_name

class Validator(object):
    __metaclass__ = abc.ABCMeta
    registry = defaultdict()

    @abc.abstractmethod
    def validate(self, delta):
        pass

    @classmethod
    def register(cls, klass):
        assert Validator in klass.mro()
        cls.registry[fully_qualified_name(klass.diff_item)] = klass

    @classmethod
    def validate_all(cls, deltas):
        for delta in deltas:
            validator = cls.registry.get(fully_qualified_name(delta.diff_item))
            if validator:
                validator().validate(delta)

    def __repr__(self):
        return '{kls} ({s})'.format(kls=(self.__class__.__name__), s=(self.__str__()))

    def __str__(self):
        return self.__repr__()