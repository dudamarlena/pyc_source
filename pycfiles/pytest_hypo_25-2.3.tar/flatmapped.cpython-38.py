# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\flatmapped.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1778 bytes
from hypothesis.internal.reflection import get_pretty_function_description
from hypothesis.internal.validation import check_type
from hypothesis.strategies._internal.strategies import SearchStrategy

class FlatMapStrategy(SearchStrategy):

    def __init__(self, strategy, expand):
        super().__init__()
        self.flatmapped_strategy = strategy
        self.expand = expand

    def calc_is_empty(self, recur):
        return recur(self.flatmapped_strategy)

    def __repr__(self):
        if not hasattr(self, '_cached_repr'):
            self._cached_repr = '%r.flatmap(%s)' % (
             self.flatmapped_strategy,
             get_pretty_function_description(self.expand))
        return self._cached_repr

    def do_draw(self, data):
        source = data.draw(self.flatmapped_strategy)
        expanded_source = self.expand(source)
        check_type(SearchStrategy, expanded_source)
        return data.draw(expanded_source)

    @property
    def branches(self):
        return [FlatMapStrategy(strategy=strategy, expand=(self.expand)) for strategy in self.flatmapped_strategy.branches]