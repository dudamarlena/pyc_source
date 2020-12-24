# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/test_constructor.py
# Compiled at: 2011-11-02 15:34:09
import pexpect, unittest, time
from . import PexpectTestCase

class TestCaseConstructor(PexpectTestCase.PexpectTestCase):

    def test_constructor(self):
        """This tests that the constructor will work and give
        the same results for different styles of invoking __init__().
        This assumes that the root directory / is static during the test.
        """
        p1 = pexpect.spawn('/bin/ls -l /bin')
        p2 = pexpect.spawn('/bin/ls', ['-l', '/bin'])
        p1.expect(pexpect.EOF)
        p2.expect(pexpect.EOF)
        assert p1.before == p2.before

    def test_named_parameters(self):
        """This tests that named parameters work.
        """
        p = pexpect.spawn('/bin/ls', timeout=10)
        p = pexpect.spawn(timeout=10, command='/bin/ls')
        p = pexpect.spawn(args=[], command='/bin/ls')


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(TestCaseConstructor, 'test')