# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/assertions_is/booleans.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 1299 bytes
from .base_is import IsBase

class __IsBool(IsBase):

    @property
    def boolean(self) -> 'Is':
        self.check.is_boolean()
        return self

    @property
    def not_boolean(self) -> 'Is':
        self.check.is_not_boolean()
        return self

    @property
    def true(self) -> 'Is':
        self.check.is_true()
        return self

    @property
    def false(self) -> 'Is':
        self.check.is_false()
        return self

    @property
    def not_true(self) -> 'Is':
        self.check.is_not_true()
        return self

    @property
    def not_false(self) -> 'Is':
        self.check.is_not_false()
        return self

    @property
    def falsy(self) -> 'Is':
        self.check.is_falsy()
        return self

    @property
    def not_falsy(self) -> 'Is':
        self.check.is_not_falsy()
        return self

    @property
    def truthy(self) -> 'Is':
        self.check.is_truthy()
        return self

    @property
    def not_truthy(self) -> 'Is':
        self.check.is_not_truthy()
        return self

    def has_same_truth_of(self, compare_obj) -> 'Is':
        self.check.has_same_truth_of(compare_obj)
        return self

    def has_opposite_truth_of(self, compare_obj) -> 'Is':
        self.check.has_opposite_truth_of(compare_obj)
        return self