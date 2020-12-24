# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\shared.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1474 bytes
from hypothesis.strategies._internal import SearchStrategy
SHARED_STRATEGY_ATTRIBUTE = '_hypothesis_shared_strategies'

class SharedStrategy(SearchStrategy):

    def __init__(self, base, key=None):
        self.key = key
        self.base = base

    @property
    def supports_find(self):
        return self.base.supports_find

    def __repr__(self):
        if self.key is not None:
            return 'shared(%r, key=%r)' % (self.base, self.key)
        return 'shared(%r)' % (self.base,)

    def do_draw(self, data):
        if not hasattr(data, SHARED_STRATEGY_ATTRIBUTE):
            setattr(data, SHARED_STRATEGY_ATTRIBUTE, {})
        sharing = getattr(data, SHARED_STRATEGY_ATTRIBUTE)
        key = self.key or self
        if key not in sharing:
            sharing[key] = data.draw(self.base)
        return sharing[key]