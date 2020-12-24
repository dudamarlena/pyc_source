# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/service/utils.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 879 bytes
from __future__ import with_statement
from common import utils

class IdGenerator:
    _IdGenerator__all_generators = {}

    def __init__(self, category='global', last_id=-1):
        self._IdGenerator__category = category
        self._IdGenerator__last_id = last_id
        IdGenerator._IdGenerator__all_generators[category] = self

    @staticmethod
    def next(category='global'):
        ig = IdGenerator._IdGenerator__all_generators.get(category, None)
        i = -1
        if isinstance(ig, IdGenerator):
            with utils.LockContext(ig):
                ig._IdGenerator__last_id += 1
                i = ig._IdGenerator__last_id
        return i

    @staticmethod
    def setup(d):
        for k, v in d.items():
            if isinstance(v, int) and isinstance(k, str):
                IdGenerator._IdGenerator__all_generators[k] = IdGenerator(category=k, last_id=v)

    @staticmethod
    def reset():
        IdGenerator._IdGenerator__all_generators.clear()