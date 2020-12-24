# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/test_dotall.py
# Compiled at: 2011-11-02 15:34:08
import pexpect, unittest, os, re
from . import PexpectTestCase
testdata = 'BEGIN\nHello world\nEND'

class TestCaseDotall(PexpectTestCase.PexpectTestCase):

    def test_dotall(self):
        p = pexpect.spawn('echo "%s"' % testdata)
        i = p.expect(['BEGIN(.*)END', pexpect.EOF])
        assert i == 0, 'DOTALL does not seem to be working.'

    def test_precompiled(self):
        p = pexpect.spawn('echo "%s"' % testdata)
        pat = re.compile('BEGIN(.*)END')
        i = p.expect([pat, pexpect.EOF])
        assert i == 1, 'Precompiled pattern to override DOTALL does not seem to be working.'


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(TestCaseDotall, 'test')