# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\shrinking\lexical.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 2055 bytes
from hypothesis.internal.compat import int_from_bytes, int_to_bytes
from hypothesis.internal.conjecture.shrinking.common import Shrinker
from hypothesis.internal.conjecture.shrinking.integer import Integer
from hypothesis.internal.conjecture.shrinking.ordering import Ordering

class Lexical(Shrinker):

    def make_immutable(self, value):
        return bytes(value)

    @property
    def size(self):
        return len(self.current)

    def check_invariants(self, value):
        assert len(value) == self.size

    def left_is_better(self, left, right):
        return left < right

    def incorporate_int(self, i):
        return self.incorporate(int_to_bytes(i, self.size))

    @property
    def current_int(self):
        return int_from_bytes(self.current)

    def minimize_as_integer(self, full=False):
        Integer.shrink((self.current_int),
          (lambda c: c == self.current_int or self.incorporate_int(c)),
          random=(self.random),
          full=full)

    def partial_sort(self):
        Ordering.shrink((self.current), (self.consider), random=(self.random))

    def short_circuit(self):
        """This is just an assemblage of other shrinkers, so we rely on their
        short circuiting."""
        return False

    def run_step(self):
        self.minimize_as_integer()
        self.partial_sort()