# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/tests/test_mp_sessions.py
# Compiled at: 2006-08-02 05:57:50
import unittest
from harold.tests.test_sessions import TestApp
session_url = 'http://localhost/harold_mod_python_session_test'

class ApacheModPythonSession_Test(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        import mechanize
        self.url = session_url
        self.browser = mechanize.Browser()

    def test_session_counter(self):
        """ match mod_python session provider output """
        count = 3
        for i in range(count):
            response = self.browser.open(self.url)
            results = response.read()

        self.failUnless(TestApp.match(results, count))


if __name__ == '__main__':
    unittest.main()