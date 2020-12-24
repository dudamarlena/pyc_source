# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\misc.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1406 bytes
from hypothesis.strategies._internal.strategies import SampledFromStrategy, is_simple_data

class JustStrategy(SampledFromStrategy):
    __doc__ = "A strategy which always returns a single fixed value.\n\n    It's implemented as a length-one SampledFromStrategy so that all our\n    special-case logic for filtering and sets applies also to just(x).\n    "

    def __init__(self, value):
        SampledFromStrategy.__init__(self, [value])

    @property
    def value(self):
        return self.elements[0]

    def __repr__(self):
        return 'just(%r)' % (self.value,)

    def calc_has_reusable_values(self, recur):
        return True

    def calc_is_cacheable(self, recur):
        return is_simple_data(self.value)

    def do_draw(self, data):
        return self.value