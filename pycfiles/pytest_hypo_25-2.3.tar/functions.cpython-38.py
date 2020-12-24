# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\functions.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1693 bytes
from hypothesis.control import note
from hypothesis.errors import InvalidState
from hypothesis.internal.reflection import arg_string, nicerepr, proxies
from hypothesis.strategies._internal.strategies import SearchStrategy

class FunctionStrategy(SearchStrategy):
    supports_find = False

    def __init__(self, like, returns):
        super().__init__()
        self.like = like
        self.returns = returns

    def calc_is_empty(self, recur):
        return recur(self.returns)

    def do_draw(self, data):

        @proxies(self.like)
        def inner(*args, **kwargs):
            if data.frozen:
                raise InvalidState('This generated %s function can only be called within the scope of the @given that created it.' % (
                 nicerepr(self.like),))
            val = data.draw(self.returns)
            note('Called function: %s(%s) -> %r' % (
             nicerepr(self.like), arg_string(self.like, args, kwargs), val))
            return val

        return inner