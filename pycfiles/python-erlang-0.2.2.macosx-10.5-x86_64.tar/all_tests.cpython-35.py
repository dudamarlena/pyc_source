# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nm46057/anaconda/lib/python3.5/site-packages/tests/all_tests.py
# Compiled at: 2016-11-26 19:03:55
# Size of source mod 2**32: 263 bytes
from erlang import extended_b_lines

class TestLineCalculation:

    def setup_class(self):
        self.cases = [
         (0.001, 8, 18), (0.5, 30, 21), (0.03, 2, 6)]

    def test_calcluations(self):
        for case in self.cases:
            if not extended_b_lines(case[1], case[0]) == case[2]:
                raise AssertionError