# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/assertions_is/sequences.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 1153 bytes
from fluentcheck.assertions_is.base_is import IsBase

class __IsSequences(IsBase):

    @property
    def empty(self) -> 'Is':
        self.check.is_empty()
        return self

    @property
    def not_empty(self) -> 'Is':
        self.check.is_not_empty()
        return self

    @property
    def iterable(self) -> 'Is':
        self.check.is_iterable()
        return self

    @property
    def not_iterable(self) -> 'Is':
        self.check.is_not_iterable()
        return self

    @property
    def couple(self) -> 'Is':
        self.check.is_couple()
        return self

    @property
    def triplet(self) -> 'Is':
        self.check.is_triplet()
        return self

    def nuple(self, dimension: int) -> 'Is':
        self.check.is_nuple(dimension)
        return self

    def has_dimensionality(self, dimensionality: int) -> 'Is':
        self.check.has_dimensionality(dimensionality)
        return self

    @property
    def tuple(self) -> 'Is':
        self.check.is_tuple()
        return self

    @property
    def list(self) -> 'Is':
        self.check.is_list()
        return self