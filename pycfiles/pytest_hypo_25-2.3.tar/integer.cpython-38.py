# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\shrinking\integer.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 2362 bytes
from hypothesis.internal.conjecture.shrinking.common import Shrinker, find_integer

class Integer(Shrinker):
    __doc__ = 'Attempts to find a smaller integer. Guaranteed things to try ``0``,\n\n    ``1``, ``initial - 1``, ``initial - 2``. Plenty of optimisations beyond\n    that but those are the guaranteed ones.\n    '

    def short_circuit(self):
        for i in range(2):
            if self.consider(i):
                return True
            self.mask_high_bits()
            if self.size > 8:
                self.consider(self.current >> self.size - 8)
                self.consider(self.current & 255)
            return self.current == 2

    def check_invariants(self, value):
        assert value >= 0

    def left_is_better(self, left, right):
        return left < right

    def run_step(self):
        self.shift_right()
        self.shrink_by_multiples(2)
        self.shrink_by_multiples(1)

    def shift_right(self):
        base = self.current
        find_integer(lambda k: k <= self.size and self.consider(base >> k))

    def mask_high_bits(self):
        base = self.current
        n = base.bit_length()

        @find_integer
        def try_mask(k):
            if k >= n:
                return False
            mask = (1 << n - k) - 1
            return self.consider(mask & base)

    @property
    def size(self):
        return self.current.bit_length()

    def shrink_by_multiples(self, k):
        base = self.current

        @find_integer
        def shrunk(n):
            attempt = base - n * k
            return attempt >= 0 and self.consider(attempt)

        return shrunk > 0