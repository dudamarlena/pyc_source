# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tests/contribs/test_tail_call_optimized.py
# Compiled at: 2016-07-19 10:55:32
from unittest import TestCase
from ycyc.contribs.tail_call_optimized import tail_call_optimized

class TestTailCallOptimized(TestCase):

    def test_usage(self):

        @tail_call_optimized
        def factorial(n, acc=1):
            """calculate a factorial"""
            if n == 0:
                return acc
            return factorial(n - 1, n * acc)

        factorial(10000)

        @tail_call_optimized
        def fib(i, current=0, next=1):
            if i == 0:
                return current
            else:
                return fib(i - 1, next, current + next)

        fib(10000)