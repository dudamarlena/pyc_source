# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/assertions_is/collections.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 1002 bytes
from typing import Any, Set
from .base_is import IsBase

class __IsCollections(IsBase):

    @property
    def set(self) -> 'Is':
        self.check.is_set()
        return self

    @property
    def not_set(self) -> 'Is':
        self.check.is_not_set()
        return self

    def subset_of(self, full_set: Set[Any]) -> 'Is':
        self.check.is_subset_of(full_set)
        return self

    def not_subset_of(self, full_set: Set[Any]) -> 'Is':
        self.check.is_not_subset_of(full_set)
        return self

    def superset_of(self, full_set: Set[Any]) -> 'Is':
        self.check.is_superset_of(full_set)
        return self

    def not_superset_of(self, subset: Set[Any]) -> 'Is':
        self.check.is_not_superset_of(subset)
        return self

    def intersects(self, other_set: Set[Any]) -> 'Is':
        self.check.intersects(other_set)
        return self

    def not_intersects(self, other_set: Set[Any]) -> 'Is':
        self.check.not_intersects(other_set)
        return self