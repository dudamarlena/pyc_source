# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/sanity_test.py
# Compiled at: 2020-05-05 05:08:14
# Size of source mod 2**32: 1031 bytes
import unittest
from test.test_utils import run_sanity_test

class SanityTest(unittest.TestCase):
    __doc__ = '\n    Test cases from https://wiki.python.org/moin/SimplePrograms\n    there is a bracket error at the start of every file to get past\n    ast.parse() check, the premise of these asd is to only detect\n    that firs error and not any other false positives\n    '

    def test_sanity(self):
        run_sanity_test(self, 'sanity_samples/sanity.py')

    def test_sanity2(self):
        run_sanity_test(self, 'sanity_samples/sanity2.py')

    def test_sanity3(self):
        run_sanity_test(self, 'sanity_samples/sanity3.py')

    def test_sanity4(self):
        run_sanity_test(self, 'sanity_samples/sanity4.py')

    def test_sanity5(self):
        run_sanity_test(self, 'sanity_samples/sanity5.py')

    def test_sanity6(self):
        run_sanity_test(self, 'sanity_samples/sanity6.py')

    def test_sanity7(self):
        run_sanity_test(self, 'sanity_samples/sanity7.py')


if __name__ == '__main__':
    unittest.main()