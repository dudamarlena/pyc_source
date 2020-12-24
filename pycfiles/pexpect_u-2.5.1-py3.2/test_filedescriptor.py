# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/test_filedescriptor.py
# Compiled at: 2011-11-02 15:34:08
import pexpect
from pexpect import fdpexpect
import unittest
from . import PexpectTestCase
import sys, os

class ExpectTestCase(PexpectTestCase.PexpectTestCase):

    def setUp(self):
        print(self.id())
        PexpectTestCase.PexpectTestCase.setUp(self)

    def test_fd(self):
        fd = os.open('TESTDATA.txt', os.O_RDONLY)
        s = fdpexpect.fdspawn(fd)
        s.expect('This is the end of test data:')
        s.expect(pexpect.EOF)
        assert s.before == ' END\n'

    def test_maxread(self):
        fd = os.open('TESTDATA.txt', os.O_RDONLY)
        s = fdpexpect.fdspawn(fd)
        s.maxread = 100
        s.expect('2')
        s.expect('This is the end of test data:')
        s.expect(pexpect.EOF)
        assert s.before == ' END\n'

    def test_fd_isalive(self):
        fd = os.open('TESTDATA.txt', os.O_RDONLY)
        s = fdpexpect.fdspawn(fd)
        assert s.isalive()
        os.close(fd)
        assert not s.isalive(), 'Should not be alive after close()'

    def test_fd_isatty(self):
        fd = os.open('TESTDATA.txt', os.O_RDONLY)
        s = fdpexpect.fdspawn(fd)
        assert not s.isatty()
        s.close()


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(ExpectTestCase, 'test')