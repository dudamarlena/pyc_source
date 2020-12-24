# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/test/cpu_test.py
# Compiled at: 2012-02-12 09:01:13
import unittest
from linseed import CPUs

class Test(unittest.TestCase):

    def test_util(self):
        """Iterating CPU utilizations."""
        c = CPUs()
        for util in c:
            pass

    def test_interval(self):
        """CPU check interval."""
        c = CPUs(0.2)
        for util in c:
            pass