# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\shrinking\ordering.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 3445 bytes
from hypothesis.internal.conjecture.shrinking.common import Shrinker, find_integer

def identity(v):
    return v


class Ordering(Shrinker):
    __doc__ = 'A shrinker that tries to make a sequence more sorted.\n\n    Will not change the length or the contents, only tries to reorder\n    the elements of the sequence.\n    '

    def setup(self, key=identity):
        self.key = key

    def make_immutable(self, value):
        return tuple(value)

    def short_circuit(self):
        return self.consider(sorted((self.current), key=(self.key)))

    def left_is_better(self, left, right):
        return tuple(map(self.key, left)) < tuple(map(self.key, right))

    def check_invariants(self, value):
        assert len(value) == len(self.current)
        assert sorted(value) == sorted(self.current)

    def run_step(self):
        self.sort_regions()
        self.sort_regions_with_gaps()

    def sort_regions(self):
        """Guarantees that for each i we have tried to swap index i with
        index i + 1.

        This uses an adaptive algorithm that works by sorting contiguous
        regions starting from each element.
        """
        i = 0
        while i + 1 < len(self.current):
            prefix = list(self.current[:i])
            k = find_integer(lambda k: i + k <= len(self.current) and self.consider(prefix + sorted((self.current[i:i + k]), key=(self.key)) + list(self.current[i + k:])))
            i += k

    def sort_regions_with_gaps(self):
        """Guarantees that for each i we have tried to swap index i with
        index i + 2.

        This uses an adaptive algorithm that works by sorting contiguous
        regions centered on each element, where that element is treated as
        fixed and the elements around it are sorted..
        """
        for i in range(1, len(self.current) - 1):
            if (self.current[(i - 1)] <= self.current[i] ) <= self.current[(i + 1)]:
                pass
            else:
                break

            def can_sort(a, b):
                if a < 0 or b > len(self.current):
                    return False
                assert a <= i < b
                split = i - a
                values = sorted(self.current[a:i] + self.current[i + 1:b])
                return self.consider(list(self.current[:a]) + values[:split] + [
                 self.current[i]] + values[split:] + list(self.current[b:]))

            left = i
            right = i + 1
            right += find_integer(lambda k: can_sort(left, right + k))
            find_integer(lambda k: can_sort(left - k, right))