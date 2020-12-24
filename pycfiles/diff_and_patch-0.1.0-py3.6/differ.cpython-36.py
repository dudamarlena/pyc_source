# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/diff_and_patch/diff/differ.py
# Compiled at: 2018-08-26 08:41:53
# Size of source mod 2**32: 1358 bytes
import logging
from diff_and_patch.delta import Delta
from diff_and_patch.diff.diff_item import DiffItem
from diff_and_patch.exceptions import NoDelta
logger = logging.getLogger(__name__)

class Differ(object):
    diffs = []

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self._diff_items = []
        for diff in self.diffs:
            assert issubclass(diff, DiffItem)
            diff_item = diff(self)
            self._diff_items.append(diff_item)

    def diff(self):
        deltas = []
        for item in self._diff_items:
            _deltas = item.deltas()
            if isinstance(_deltas, Delta):
                _deltas = [
                 _deltas]
            if _deltas:
                deltas += _deltas

        if not deltas:
            raise NoDelta()
        logger.info('{i} deltas detected'.format(i=('\n'.join(map(str, deltas)))))
        return deltas

    def __repr__(self):
        return '{kls}: ({lhs}, {rhs} \n {d})'.format(kls=(self.__class__.__name__), lhs=(self.lhs),
          rhs=(self.rhs),
          d=(','.join(self._diff_items)))

    def __str__(self):
        return str(self.__class__.__name__)