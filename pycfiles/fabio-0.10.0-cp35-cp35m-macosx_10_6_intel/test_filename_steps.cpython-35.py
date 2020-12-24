# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_filename_steps.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 2705 bytes
"""
Test cases for the Next/Previous ...

28/11/2014
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, logging
logger = logging.getLogger(__name__)
import fabio

class TestNext(unittest.TestCase):

    def test_next1(self):
        files = [
         [
          'data0001.edf', 'data0002.edf'],
         [
          'bob1.edf', 'bob2.edf'],
         [
          '1.edf', '2.edf'],
         [
          '1.mar2300', '2.mar2300']]
        for name, next_ in files:
            self.assertEqual(next_, fabio.next_filename(name))


class TestPrev(unittest.TestCase):

    def test_prev1(self):
        files = [
         [
          'data0001.edf', 'data0000.edf'],
         [
          'bob1.edf', 'bob0.edf'],
         [
          '1.edf', '0.edf'],
         [
          '1.mar2300', '0.mar2300']]
        for name, prev in files:
            self.assertEqual(prev, fabio.previous_filename(name))


class TestJump(unittest.TestCase):

    def test_jump1(self):
        files = [
         [
          'data0001.edf', 'data99993.edf', 99993],
         [
          'bob1.edf', 'bob0.edf', 0],
         [
          '1.edf', '123456.edf', 123456],
         [
          'mydata001.mar2300.gz', 'mydata003.mar2300.gz', 3]]
        for name, res, num in files:
            self.assertEqual(res, fabio.jump_filename(name, num))


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestNext))
    testsuite.addTest(loadTests(TestPrev))
    testsuite.addTest(loadTests(TestJump))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())